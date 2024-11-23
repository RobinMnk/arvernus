import queue
import threading
from time import sleep

from src.api import Client
from src.api.runner.models import Scenario, Vehicle, VehicleUpdate
from src.arvernus.strategy.base_strategy import BaseStrategy


class Schedule:
    _schedule: list[list[int]]

    def __init__(self, num_vehicles):
        self._schedule = [list() for _ in range(num_vehicles)]


class AnnouncementPlan:
    _lock = threading.Lock()
    _plan: list[tuple[int, VehicleUpdate]]

    def update(self, ap: list[tuple[int, VehicleUpdate]]):
        with self._lock:
            self._plan = ap

    def get(self):
        with self._lock:
            return self._plan


class Arvernus:
    schedule: Schedule
    scenario: Scenario
    state_queue: queue.Queue[Vehicle]
    ap: AnnouncementPlan

    def __init__(self, state_queue: queue.Queue[Vehicle], ap: AnnouncementPlan):
        self.state_queue = state_queue
        self.announce_plan = ap

    def init_scenario(self, scenario: Scenario):
        self.scenario = scenario

    def compute_assigment(self):
        """ use VRP solver"""
        # init instance
        # solve instance
        # extract paths
        # compute schedule
        # convert to AP
        # set AP
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
        pass

    def update_schedule(self):
        return self.schedule


class Announcer(BaseStrategy):
    arv: Arvernus
    announcement_plan: AnnouncementPlan

    def __init__(self, client: Client, scenario: Scenario) -> None:
        super().__init__(client, scenario)

        self.announcement_plan = AnnouncementPlan()
        self.arv = Arvernus(self.state_queue, self.announcement_plan)
        self.init_scenario(scenario)

        thread = threading.Thread(target=self.arv.refinement_loop)
        self.threads.append(thread)
        thread.start()

    def init_scenario(self, scenario: Scenario):
        self.scenario = scenario
        self.arv.init_scenario(scenario)

    def strategy_loop(self):
        while any([customer for customer in self.scenario.customers if customer.awaiting_service]):
            ap = self.announcement_plan.get()

            # while ap[-1][0] > current_time:



            sleep(1) # busy wait


    def _push_updates(self):
        """ push update to out-queue"""
        pass
