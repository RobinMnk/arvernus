from http import HTTPStatus
from queue import Queue
import logging
import random
import threading
from threading import Thread
from abc import ABC, abstractmethod

from api.client import Client
from api.runner.api.runner import post_launch_scenario
from api.runner.api.scenarios import get_get_scenario, post_initialize_scenario, put_update_scenario
from api.runner.models.customer import Customer
from api.runner.models.scenario import Scenario
from api.runner.models.update_scenario import UpdateScenario
from api.runner.models.vehicle import Vehicle
from api.runner.models.vehicle_update import VehicleUpdate


class BaseStrategy(ABC):
    client: Client
    threads: list[Thread]

    scenario_id: str
    waiting_customers: list[Customer]

    state_queue: Queue[Vehicle]
    update_queue: Queue[UpdateScenario]

    def __init__(self, client: Client, scenario: Scenario) -> None:
        super().__init__()

        self.client = client
        self.scenario_id = scenario.id

    def start(self, scenario: Scenario):
        self.waiting_customers = scenario.customers
        self.threads = []

        self.state_queue = Queue()
        self.update_queue = Queue()

        initialize = post_initialize_scenario.sync_detailed(client=self.client, body=scenario)
        assert initialize.status_code == HTTPStatus.OK

        launch = post_launch_scenario.sync_detailed(client=self.client, speed=0.2, scenario_id=scenario.id)
        assert launch.status_code == HTTPStatus.OK

        vehicles = launch.parsed.vehicles  # TODO

        for vehicle in vehicles:
            self.state_queue.put(vehicle)

        thread = threading.Thread(target=self.strategy_loop)
        self.threads.append(thread)
        thread.start()

    @abstractmethod
    def strategy_loop(self):
        pass

    def loop(self):
        while len(self.waiting_customers) > 0:
            update = self.update_queue.get()
            response = put_update_scenario.sync_detailed(client=self.client, scenario_id=self.scenario_id, body=update)

            updated_vehicles = [Vehicle.from_dict(vehicle) for vehicle in response.parsed.updatedVehicles]  # TODO

            for vehicle in updated_vehicles:
                self.state_queue.put(vehicle)

        for thread in self.threads:
            thread.join()


class RandomStrategy(BaseStrategy):
    def __init__(self, client: Client, scenario: Scenario) -> None:
        super().__init__(client, scenario)

    def step(self, scenario: Scenario):
        while len(self.waiting_customers) > 0:
            response = get_get_scenario.sync_detailed(client=self.client, scenario_id=self.scenario_id)
            scenario = Scenario.from_dict(response.parsed)

            waiting_vehicles = [vehicle for vehicle in scenario.vehicles if vehicle.is_waing]

            assigned_customers = random.sample(self.waiting_customers, len(waiting_vehicles))
            self.waiting_customers -= assigned_customers

            vehicle_updates = []
            for vehicle, customer in zip(waiting_vehicles, assigned_customers):
                logging.info(f"Assigning vehicle {vehicle.id} to customer {customer.id}")
                vehicle_updates.append(VehicleUpdate(vehicle.id, customer.id))
            update = UpdateScenario(vehicle_updates)

            self.update_queue.put(update)
