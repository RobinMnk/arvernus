import queue
import threading
from time import sleep

from src.api import Client
from src.api.runner.models import Scenario, Vehicle, VehicleUpdate
from src.arvernus.strategy.base_strategy import BaseStrategy

from networkx import from_numpy_matrix, relabel_nodes, DiGraph
from geopy.distance import geodesic


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
        customers = scenario.customers
        vehicles = scenario.vehicles
        # compute distances + add to adjacency matrix (one start point and end point per costumer)
        nodeNumber = len(vehicles)+2*len(customers)
        distanceMatrix = np.zeros((nodeNumber,nodeNumber))
        
        countVehicles = len(vehicles)
        countCostumers = len(customers)
        
        for v in range(1,countVehicles):
            G.add_edge("Source", v, cost=0, time=1)
        
        for i  in range(1,countCostumers):
            distance = geodesic(customers(i)(coord_x,coord_y), customers(i)(destination_x,destination_y)).km
            G.add_edge(countVehicles+2*i-1,countVehicles+2*i, cost=distance, time=2)
            
            for j in range(1,countVehicles):
                distanceStart = geodesic(vehicles(j)(ccord_x,coord_y), customers(i)(coord_x,coord_y)).km
                G.add_edge(j,countVehicles+2*i-1, cost=distanceStart, time=2)
                
            
            for k in range(i+1,countCostumers):
                distanceToOther = geodesic(customers(i)(destination_x,destination_y),customers(k)(coord_x,coord_y)).km
                G.add_edge(countVehicles+2*i,countVehicles+2*k-1, cost=distanceToOther, time=2)
            
                distanceFromOther = geodesic(customers(i)(coord_x,coord_y),customers(k)(destination_x,destination_y)).km
                G.add_edge(countVehicles+2*k,countVehicles+2*i-1, cost=distanceToOther, time=2)
            
            G.add_edge(countVehicles+2*i-1, "Sink", cost = 0, time = 0)
        
        for i in range(1,countCostumers):
            G.nodes[countVehicles+2*i-1]["request"] = countVehicles+2*i
            G.nodes[countVehicles+2*i-1]["demand"] = 1]
            G.nodes[countVehicles+2*i]["demand"] = -1]
    
        for j in range(1,countVehicles):
            G.nodes[j]["lower"] = 0
            G.nodes[j]["upper"] = 2
    
        
        # solve instance
        prob = VehicleRoutingProblem(G, load_capacity=1, pickup_delivery=True, time_windows = True, num_vehicles = countVehicles)
        
        prob.solve(cspy=False)
        # extract paths
        
        paths = prob.best_routes
        
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
