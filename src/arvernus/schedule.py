import queue
import threading
from collections import namedtuple
from time import sleep, time
from geopy.distance import geodesic

from api.runner.models import UpdateScenario, Customer
from src.api import Client
from src.api.runner.models import Scenario, Vehicle, VehicleUpdate
from src.arvernus.strategy.base_strategy import BaseStrategy


class Schedule:
    _schedule: list[list[int]]

    def __init__(self, num_vehicles):
        self._schedule = [list() for _ in range(num_vehicles)]


class AnnouncementPlan:
    _lock = threading.Lock()
    _plan: list[tuple[float, VehicleUpdate]]

    def from_schedule(self, schedule: Schedule, simulation_speed: float, start_time):
        # TODO: ap = convert schedule to ap
        # self.update(ap)
        pass

    def update(self, ap: list[tuple[int, VehicleUpdate]]):
        with self._lock:
            self._plan = ap

    def get(self):
        with self._lock:
            return self._plan


def get_distance_in_meter(customer: Customer):
    return geodesic((customer.coord_x, customer.coord_y), (customer.destination_x, customer.destination_y)).m


VehicleAvailability = namedtuple("VehicleAvailability", "time, posX, posY")
Assignment = namedtuple("Assignment", "time, cIx")


class Arvernus:
    schedule: Schedule
    scenario: Scenario
    state_queue: queue.Queue[Vehicle]
    ap: AnnouncementPlan
    sim_speed: float
    start_time: float
    av_veh: dict[str: VehicleAvailability]  # vehicle id -> time, posX, posY
    assignments: dict[str: Assignment]  # vehicle id -> time, cIx

    def __init__(self, state_queue: queue.Queue[Vehicle], ap: AnnouncementPlan):
        self.state_queue = state_queue
        self.announce_plan = ap

    def init_scenario(self, scenario: Scenario, start_time: float, sim_speed: float):
        self.scenario = scenario
        self.start_time = start_time
        self.sim_speed = sim_speed
        self.av_veh = {v.id: (start_time, v.coord_x, v.coord_y) for v in scenario.vehicles}

    def compute_assigment(self):
        """ use VRP solver"""
        # init instance
        # solve instance
        # extract paths
        # compute schedule
        # convert to AP
        # set AP, av_veh, current_assignment
        pass

    def refinement_loop(self):
        while True:
            try:
                moved_vehicle = self.state_queue.get()  # blocking call -> wait for updates
                self.process_update(moved_vehicle)
            except queue.Empty:
                return

    def process_update(self, moved_vehicle: Vehicle):
        # local updates to schedule
        vId = moved_vehicle.id
        asm = self.assignments[vId]
        csm = self.scenario.customers[asm.cIx]
        dst = get_distance_in_meter(csm)

        self.av_veh[vId] = (
            asm.time + dst / moved_vehicle.vehicle_speed * self.sim_speed,
            csm.destination_x, csm.destination_y
        )


class Announcer(BaseStrategy):
    arv: Arvernus
    announcement_plan: AnnouncementPlan
    start_time: float
    sim_speed: float

    def __init__(self, client: Client, scenario: Scenario) -> None:
        super().__init__(client, scenario)

        self.announcement_plan = AnnouncementPlan()
        self.arv = Arvernus(self.state_queue, self.announcement_plan)

        thread = threading.Thread(target=self.arv.refinement_loop)
        thread.start()

    def init_scenario(self, scenario: Scenario, sim_speed: float):
        self.scenario = scenario
        self.sim_speed = sim_speed
        self.start_time = time()
        self.arv.init_scenario(scenario, self.start_time, sim_speed)
        self.arv.compute_assigment()

    def run(self, speed=0.2):
        self.init_scenario(self.scenario, speed)
        super().run(speed)

    def strategy_loop(self):
        while any([customer for customer in self.scenario.customers if customer.awaiting_service]):
            ap = self.announcement_plan.get()

            if not ap:
                continue

            current_time = (time() - self.start_time) / (self.sim_speed + 1e-12)

            pending_updates = [
                VehicleUpdate(self.scenario.vehicles[vIx].id, self.scenario.customers[cIx].id)
                for tm, (vIx, cIx) in ap if tm >= current_time
            ]

            update = UpdateScenario(pending_updates)
            self.update_queue.put(update)

            sleep(0.1)  # busy wait


