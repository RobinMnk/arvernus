from http import HTTPStatus
from queue import Queue
import logging
import queue
import random
import threading
from threading import Thread
from abc import ABC, abstractmethod
from typing import override
from time import sleep

from api.client import Client
from api.runner.api.runner import post_launch_scenario
from api.runner.api.scenarios import get_get_scenario, post_initialize_scenario, put_update_scenario
from api.runner.models.scenario import Scenario
from api.runner.models.update_scenario import UpdateScenario
from api.runner.models.vehicle import Vehicle
from api.runner.models.vehicle_update import VehicleUpdate

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class BaseStrategy(ABC):
    client: Client
    api_thread: Thread | None

    scenario: Scenario
    sim_speed: float

    state_queue: Queue[Vehicle]
    update_queue: Queue[UpdateScenario]

    def __init__(self, client: Client, scenario: Scenario) -> None:
        super().__init__()

        self.client = client
        self.scenario = scenario
        self.api_thread = None

    def run(self):
        self.threads = []
        self.sim_speed = 5

        self.state_queue = Queue()
        self.update_queue = Queue()

        initialize = post_initialize_scenario.sync_detailed(client=self.client, body=self.scenario)
        assert initialize.status_code == HTTPStatus.OK
        sleep(3)

        launch = post_launch_scenario.sync_detailed(client=self.client, speed=self.sim_speed, scenario_id=self.scenario.id)
        assert launch.status_code == HTTPStatus.OK
        logging.info(f"Launched scenario: {launch}")

        response = get_get_scenario.sync_detailed(client=self.client, scenario_id=self.scenario.id)
        self.scenario = Scenario.from_response(response)

        vehicles = self.scenario.vehicles

        for vehicle in vehicles:
            self.state_queue.put(vehicle)

        self.api_thread = threading.Thread(target=self.loop)
        self.api_thread.start()

        self.strategy_loop()

    @abstractmethod
    def running(self) -> bool:
        pass

    @abstractmethod
    def strategy_loop(self):
        pass

    def loop(self):
        assert self.scenario.status == "RUNNING"
        logging.info(f"Started api loop")

        while self.running():
            try:
                update = self.update_queue.get(timeout=0.1)
                if update:
                    logging.info(f"Update: {update}")

                    response = put_update_scenario.sync_detailed(client=self.client, scenario_id=self.scenario.id, body=update)
                    logging.info(f"Got updates {response}")
                    updated_vehicles = Vehicle.from_updated_response(response)

                    for vehicle in updated_vehicles:
                        self.state_queue.put(vehicle)
            except queue.Empty:
                pass

        logging.info("api loop terminated")


class RandomStrategy(BaseStrategy):
    def __init__(self, client: Client, scenario: Scenario) -> None:
        super().__init__(client, scenario)

    @override
    def running(self) -> bool:
        return self.scenario.status == "RUNNING"

    @override
    def strategy_loop(self):
        assert self.scenario.status == "RUNNING"
        logging.info(f"Started strategy loop")

        while self.scenario.status == "RUNNING":
            response = get_get_scenario.sync_detailed(client=self.client, scenario_id=self.scenario.id)
            self.scenario = Scenario.from_response(response)
            logging.info(f"Got scenario {self.scenario}")

            waiting_vehicles = [vehicle for vehicle in self.scenario.vehicles if vehicle.is_available]
            waiting_customers = [customer for customer in self.scenario.customers if (customer.awaiting_service and not any([vehicle.customer_id == customer.id for vehicle in self.scenario.vehicles]))]

            logging.info(f"Waiting vehicles {waiting_vehicles}")
            logging.info(f"Waiting customers {waiting_customers}")

            assigned_customers = random.sample(list(waiting_customers), min(len(waiting_vehicles), len(waiting_customers)))

            if len(assigned_customers) > 0:
                vehicle_updates = []
                for vehicle, customer in zip(waiting_vehicles, assigned_customers):
                    logging.info(f"Assigning vehicle {vehicle.id} to customer {customer.id}")
                    vehicle_updates.append(VehicleUpdate(vehicle.id, customer.id))
                update = UpdateScenario(vehicle_updates)

                self.update_queue.put(update)

            sleep(1)

        logging.info(f"Simulation finished")
        self.api_thread.join()
