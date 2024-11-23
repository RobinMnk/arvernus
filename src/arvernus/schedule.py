import queue
import threading
from collections import namedtuple
from time import sleep, time

import networkx as nx
from vrpy import VehicleRoutingProblem

from api.runner.models import UpdateScenario, Customer
from src.api import Client
from src.api.runner.models import Scenario, Vehicle, VehicleUpdate
from src.arvernus.strategy.base_strategy import BaseStrategy

from geopy.distance import geodesic


class Schedule:
    _schedule: list[list[int]]

    def __init__(self, num_vehicles):
        self._schedule = [list() for _ in range(num_vehicles)]


class AnnouncementPlan:
    _lock = threading.Lock()
    _plan: list[tuple[float, VehicleUpdate]]

    def from_schedule(self, schedule: Schedule, scenario: Scenario, simulation_speed: float, start_time, G: nx.DiGraph):
        vehicles = scenario.vehicles
        vehicleCount = len(vehicles)
        customers = scenario.customers
        
        for i in range(schedule):
            vehicleID = vehicles[i].id
            
            sendTime = start_time
            for node in schedule[i]:
                nodeID = customers[node-vehicleCount]
                self._plan.append(sendTime,(vehicleID,customerID))
                sendTime = sendTime + (G.get_edge_data(i,node)["cost"] + G.get_edge_data(node,node+1)["cost"])/8.33

        self._plan.sort(key=lambda x: x[0])
            
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


    def compute_VRP(self):
        customers = self.scenario.customers
        vehicles = self.scenario.vehicles
        # compute distances + add to adjacency matrix (one start point and end point per costumer)
        countVehicles = len(vehicles)
        countCostumers = len(customers)

        G = nx.DiGraph()
        for v in range(countVehicles):
            G.add_edge("Source", v, cost=0, time=1)

        for i  in range(countCostumers):
            distance = get_distance_in_meter(customers[i])
            G.add_edge(countVehicles+2*i,countVehicles+2*i+1, cost=distance, time=2)

            for j in range(countVehicles):
                distanceStart = geodesic((vehicles[j].coord_x,vehicles[j].coord_y), (customers[i].coord_x,customers[i].coord_y)).m
                G.add_edge(j,countVehicles+2*i, cost=distanceStart, time=2)


            for k in range(i+1,countCostumers):
                distanceToOther = geodesic((customers[i].destination_x,customers[i].destination_y),(customers[k].coord_x,customers[k].coord_y)).m
                G.add_edge(countVehicles+2*i+1,countVehicles+2*k, cost=distanceToOther, time=2)

                distanceFromOther = geodesic((customers[i].coord_x,customer[i].coord_y),(customers[k].destination_x,customers[k].destination_y)).m
                G.add_edge(countVehicles+2*k+1,countVehicles+2*i, cost=distanceFromOther, time=2)

            G.add_edge(countVehicles+2*i, "Sink", cost=0, time=10)

        for i in range(countCostumers):
            G.nodes[countVehicles+2*i]["request"] = countVehicles+2*i+1
            G.nodes[countVehicles+2*i]["demand"] = 1
            G.nodes[countVehicles+2*i+1]["demand"] = -1

        for j in range(countVehicles):
            G.nodes[j]["lower"] = 0
            G.nodes[j]["upper"] = 2


        # solve instance
        prob = VehicleRoutingProblem(G, load_capacity=1, pickup_delivery=True, time_windows = True, num_vehicles = countVehicles)

        prob.solve(cspy=False)
        # extract paths

        paths = prob.best_routes
        
        return paths, G

    def compute_assigment(self):
        """ use VRP solver"""
        # init instance
        # compute schedule
        # convert to AP
        paths, G = self.compute_VRP()
        
        for allNodesVisited in paths.values():
            vehicleNumber = allNodesVisited[1]
            del allNodesVisited[-1]
            del allNodesVisited[0]
            del allNodesVisited[0]
            
            self.schedule[vehicleNumber] = allNodesVisited
        
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


