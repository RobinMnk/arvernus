from http import HTTPStatus
from queue import Queue
import logging
import random
import threading
from threading import Thread
from abc import ABC, abstractmethod
from typing import override
import json
from time import sleep

from api.client import Client
from api.runner.api.runner import post_launch_scenario
from api.runner.api.scenarios import get_get_scenario, post_initialize_scenario, put_update_scenario
from api.runner.models.customer import Customer
from api.runner.models.scenario import Scenario
from api.runner.models.update_scenario import UpdateScenario
from api.runner.models.vehicle import Vehicle
from api.runner.models.vehicle_update import VehicleUpdate

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class BaseStrategy(ABC):
    client: Client
    threads: list[Thread]

    scenario: Scenario
    sim_speed: float

    state_queue: Queue[Vehicle]
    update_queue: Queue[UpdateScenario]

    def __init__(self, client: Client, scenario: Scenario) -> None:
        super().__init__()

        self.client = client
        self.scenario = scenario

    def run(self):
        self.threads = []
        self.sim_speed = 5

        self.state_queue = Queue()
        self.update_queue = Queue()

        initialize = post_initialize_scenario.sync_detailed(client=self.client, body=self.scenario)
        assert initialize.status_code == HTTPStatus.OK

        launch = post_launch_scenario.sync_detailed(client=self.client, speed=self.sim_speed, scenario_id=self.scenario.id)
        assert launch.status_code == HTTPStatus.OK

        vehicles = self.scenario.vehicles

        for vehicle in vehicles:
            self.state_queue.put(vehicle)

        thread = threading.Thread(target=self.strategy_loop)
        self.threads.append(thread)
        thread.start()

        self.loop()

    @abstractmethod
    def strategy_loop(self):
        pass

    def loop(self):
        logging.info(f"Started api loop")

        while any([customer for customer in self.scenario.customers if customer.awaiting_service]):
            update = self.update_queue.get()
            logging.info(update)

            response = put_update_scenario.sync_detailed(client=self.client, scenario_id=self.scenario.id, body=update)

            logging.info(response)
            updated_vehicles_raw = response.content.decode("UTF-8")
            updated_vehicles_decoded = json.loads(updated_vehicles_raw)
            updated_vehicles = [Vehicle.from_dict(vehicle) for vehicle in updated_vehicles_decoded["updatedVehicles"]]

            for vehicle in updated_vehicles:
                self.state_queue.put(vehicle)

        for thread in self.threads:
            thread.join()


class RandomStrategy(BaseStrategy):
    def __init__(self, client: Client, scenario: Scenario) -> None:
        super().__init__(client, scenario)

    @override
    def strategy_loop(self):
        logging.info(f"Started strategy loop")

        while any([customer for customer in self.scenario.customers if customer.awaiting_service]):
            response = get_get_scenario.sync_detailed(client=self.client, scenario_id=self.scenario.id)
            scenario_raw = response.content.decode("UTF-8")
            self.scenario = Scenario.from_dict(json.loads(scenario_raw))

            logging.info(f"Got scenario {self.scenario}")

            waiting_vehicles = [vehicle for vehicle in self.scenario.vehicles if vehicle.vehicle_speed == None]
            waiting_customers = [customer for customer in self.scenario.customers if (customer.awaiting_service and not any([vehicle.customer_id == customer.id for vehicle in self.scenario.vehicles]))]

            logging.info(f"Waiting vehicles {waiting_vehicles}")
            logging.info(f"Waiting customers {waiting_customers}")

            assigned_customers = random.sample(list(waiting_customers), len(waiting_vehicles))

            if len(waiting_vehicles) > 0:
                vehicle_updates = []
                for vehicle, customer in zip(waiting_vehicles, assigned_customers):
                    logging.info(f"Assigning vehicle {vehicle.id} to customer {customer.id}")
                    vehicle_updates.append(VehicleUpdate(vehicle.id, customer.id))
                update = UpdateScenario(vehicle_updates)

                self.update_queue.put(update)

            sleep(1)
