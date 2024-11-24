from geopy.distance import geodesic
from matching.games import HospitalResident, StableMarriage
from api.runner.models.customer import Customer
from api.runner.models.vehicle import Vehicle
import logging
from time import sleep
from typing_extensions import override

from api.client import Client
from api.runner.api.scenarios import get_get_scenario
from api.runner.models.scenario import Scenario
from api.runner.models.update_scenario import UpdateScenario
from api.runner.models.vehicle_update import VehicleUpdate
from arvernus.strategy.base_strategy import BaseStrategy


class MatchingStrategy(BaseStrategy):
    def __init__(self, client: Client, scenario: Scenario) -> None:
        super().__init__(client, scenario)

    @override
    def running(self) -> bool:
        return self.scenario.status == "RUNNING"

    @override
    def strategy_loop(self, speed):
        assert self.scenario.status == "RUNNING"
        logging.info(f"Started strategy loop")

        while self.scenario.status == "RUNNING":
            response = get_get_scenario.sync_detailed(client=self.client, scenario_id=self.scenario.id)
            self.scenario = Scenario.from_response(response)
            logging.info(f"Got scenario {self.scenario}")

            waiting_customers = [customer_index for customer_index, customer in enumerate(self.scenario.customers) if (customer.awaiting_service and not any([vehicle.customer_id == customer.id for vehicle in self.scenario.vehicles]))]
            idle_vehilces = [vehicle_index for vehicle_index, vehicle in enumerate(self.scenario.vehicles) if vehicle.is_available]

            result = dict(self.match())
            matching = {str(k): str(v[0]) for k, v in result.items() if len(v) > 0}

            # logging.info(f"Found matching {matching}")
            # logging.info(f"Wating customers {waiting_customers}")
            # logging.info(f"Idle vehicles {idle_vehilces}")

            vehicle_updates = []
            for vehicle_index in idle_vehilces:
                if str(vehicle_index) in matching:
                    customer_index = int(matching[str(vehicle_index)])
                    vehicle = self.scenario.vehicles[vehicle_index]
                    customer = self.scenario.customers[customer_index]

                    # logging.info(f"Vehicles {self.scenario.vehicles}, customers {self.scenario.customers}")
                    # logging.info(f"Vehicle index {vehicle_index}, customer index {customer_index}")
                    logging.info(f"Assigning vehicle {vehicle.id} to customer {customer.id}")
                    vehicle_updates.append(VehicleUpdate(vehicle.id, customer.id))
            update = UpdateScenario(vehicle_updates)

            if len(vehicle_updates) > 0:
                self.update_queue.put(update)

            sleep(5 * speed)

        logging.info(f"Simulation finished")
        self.api_thread.join()

    def match(self):
        resident_preferences = {}
        hospital_preferences = {}

        waiting_customers = [customer for customer in self.scenario.customers if customer.awaiting_service and not any([vehicle for vehicle in self.scenario.vehicles if vehicle.customer_id == customer.id])]

        for customer in waiting_customers:
            sorted = self.scenario.vehicles.copy()
            sorted.sort(key=lambda v: customer_reach_distance_m(v, customer))
            resident_preferences[self.scenario.customers.index(customer)] = [self.scenario.vehicles.index(vehicle) for vehicle in sorted]

        hospital_preferences = {}
        for vehicle in self.scenario.vehicles:
            hospital_preferences[self.scenario.vehicles.index(vehicle)] = [self.scenario.customers.index(customer) for customer in waiting_customers]

        # logging.info(f"Customer preferences {resident_preferences}")
        # logging.info(f"Vehicle preferences {hospital_preferences}")

        capacities = [1.0 for vehicle in self.scenario.vehicles]

        solver = HospitalResident.create_from_dictionaries(resident_preferences, hospital_preferences, capacities)
        matching = solver.solve()

        return matching


def customer_reach_distance_m(vehicle: Vehicle, end: Customer):
    return geodesic((vehicle.coord_x, vehicle.coord_y), (end.coord_x, end.coord_y)).m


# def travel_distance_m(customer: Customer):
#     return geodesic((customer.coord_x, customer.coord_y), (customer.destination_x, customer.destination_y)).m


# def approach_distance_m(vehicle: Vehicle, customer: Customer):
#     return geodesic((vehicle.coord_x, vehicle.coord_y), (customer.destination_x, customer.destination_y)).m


# def end_to_next_distance_m(start: Customer, end: Customer):
#     return geodesic((start.destination_x, start.destination_y), (end.coord_x, end.coord_y)).m
