import queue
import threading
from collections import namedtuple
from time import sleep, time
from pulp import logging
from typing_extensions import override

import networkx as nx
from vrpy import VehicleRoutingProblem

from api.runner.models import UpdateScenario, Customer
from api import Client
from api.runner.models import Scenario, Vehicle, VehicleUpdate
from arvernus.strategy.base_strategy import BaseStrategy

from geopy.distance import geodesic


class Schedule:
    _schedule: dict[str, list[int]]

    def __init__(self, num_vehicles):
        self._schedule = {str: list() for _ in range(num_vehicles)}

    def get(self):
        return self._schedule


class AnnouncementPlan:
    _lock = threading.Lock()
    _plan: dict[str, tuple[float, int]] = {}

    def from_schedule(self, schedule: Schedule, scenario: Scenario, simulation_speed: float, start_time, G: nx.DiGraph):
        vehicles = scenario.vehicles
        vehicleCount = len(vehicles)
        customers = scenario.customers

        ap = dict()

        sendTime = start_time
        for vId, plan in schedule.get():
            if plan:
                ap[vId] = (sendTime, plan[0])
            else:
                if vId in ap:
                    del ap[vId]
            # sendTime = sendTime + (G.get_edge_data(i, node)["cost"] + G.get_edge_data(node, node+1)["cost"]) / 8.33 * simulation_speed

        ap.sort(key=lambda x: x[0])
        self.update(ap)

    def replace(self, vId: str, timestamp: float, cIx: int):
        ap = {x: self._plan[x] for x in self._plan.keys()}
        ap[vId] = (timestamp, cIx)
        self.update(ap)

    def update(self, ap: dict[str, tuple[float, int]]):
        with self._lock:
            self._plan = ap

    def get(self):
        with self._lock:
            return self._plan


def customer_reach_distance_m(posX: float, posY: float, end: Customer):
    return geodesic((posX, posY), (end.coord_x, end.coord_y)).m


def travel_distance_m(customer: Customer):
    return geodesic((customer.coord_x, customer.coord_y), (customer.destination_x, customer.destination_y)).m


def approach_distance_m(vehicle: Vehicle, customer: Customer):
    return geodesic((vehicle.coord_x, vehicle.coord_y), (customer.destination_x, customer.destination_y)).m


def end_to_next_distance_m(start: Customer, end: Customer):
    return geodesic((start.destination_x, start.destination_y), (end.coord_x, end.coord_y)).m


VehicleAvailability = namedtuple("VehicleAvailability", "time, posX, posY")
Assignment = namedtuple("Assignment", "time, cIx")  # time the assignment was made


class Arvernus:
    schedule: Schedule
    scenario: Scenario
    state_queue: queue.Queue[Vehicle]
    ap: AnnouncementPlan
    sim_speed: float
    start_time: float
    av_veh: dict[str:VehicleAvailability]  # vehicle id -> time, posX, posY

    unassigned_customers: list[bool]
    sent_messages: int

    def __init__(self, state_queue: queue.Queue[Vehicle], ap: AnnouncementPlan):
        self.state_queue = state_queue
        self.ap = ap

    def init_scenario(self, scenario: Scenario, start_time: float, sim_speed: float):
        self.scenario = scenario
        self.schedule = Schedule(len(scenario.vehicles))
        self.start_time = start_time
        self.sim_speed = sim_speed
        self.av_veh = {v.id: (start_time, v.coord_x, v.coord_y) for v in scenario.vehicles}
        self.unassigned_customers = [True] * len(self.scenario.customers)
        self.sent_messages = 0

    def compute_VRP(self):
        customers = self.scenario.customers
        vehicles = self.scenario.vehicles
        # compute distances + add to adjacency matrix (one start point and end point per costumer)
        countVehicles = len(vehicles)
        countCostumers = len(customers)

        G = nx.DiGraph()
        for v in range(countVehicles):
            G.add_edge("Source", v, cost=10)

        for i in range(countCostumers):
            distance = travel_distance_m(customers[i])
            G.add_edge(countVehicles + 2 * i, countVehicles + 2 * i + 1, cost=distance)

            for j in range(countVehicles):
                distanceStart = approach_distance_m(vehicles[j], customers[i])
                G.add_edge(j, countVehicles + 2 * i, cost=distanceStart)

            for k in range(i + 1, countCostumers):
                distanceToOther = end_to_next_distance_m(customers[i], customers[k])
                G.add_edge(countVehicles + 2 * i + 1, countVehicles + 2 * k, cost=distanceToOther)

                distanceFromOther = geodesic((customers[i].coord_x, customers[i].coord_y), (customers[k].destination_x, customers[k].destination_y)).m
                G.add_edge(countVehicles + 2 * k + 1, countVehicles + 2 * i, cost=distanceFromOther)

            G.add_edge(countVehicles + 2 * i, "Sink", cost=5)

        for i in range(countCostumers):
            G.nodes[countVehicles + 2 * i]["request"] = countVehicles + 2 * i + 1
            G.nodes[countVehicles + 2 * i]["demand"] = 1
            G.nodes[countVehicles + 2 * i + 1]["demand"] = -1

        # for j in range(countVehicles):
        #     G.nodes[j]["lower"] = 0
        #     G.nodes[j]["upper"] = 2

        # solve instance
        prob = VehicleRoutingProblem(
            G,
            load_capacity=1,
            pickup_delivery=True,
            time_windows=False,
            num_vehicles=countVehicles,
        )

        prob.solve(cspy=False, pricing_strategy="Hyper")
        # extract paths

        paths = prob.best_routes

        return paths, G

    def compute_assignment_old(self):
        """use VRP solver"""
        # compute schedule
        # self.schedule = self.compute_VRP()
        # convert to AP
        paths, G = self.compute_VRP()

        for allNodesVisited in paths.values():
            vehicleNumber = allNodesVisited[1]
            self.schedule.get()[vehicleNumber] = [node - len(self.scenario.vehicles) for node in allNodesVisited[2:-1]]

        self.ap.from_schedule(self.schedule, self.scenario, self.sim_speed, self.start_time, G)

        # set AP, current_assignment

    def compute_initial_assignment(self):
        unassigned_vehicles = [True] * len(self.scenario.vehicles)

        positions = [(v.coord_x, v.coord_y) for v in self.scenario.vehicles]
        times = [self.start_time] * len(self.scenario.vehicles)

        to_announce = list()
        blocked = set()
        blocked_vehicles = set()

        while any(unassigned_vehicles) and any(self.unassigned_customers):
            best_option = (self.start_time + 173345345, -1, -1)
            for cIx, customer in enumerate(self.scenario.customers):
                if not self.unassigned_customers[cIx] or cIx in blocked:
                    continue
                for vIx, vehicles in enumerate(self.scenario.vehicles):
                    if vIx in blocked_vehicles:
                        continue
                    posX, posY = positions[vIx]
                    d = customer_reach_distance_m(posX, posY, customer)
                    arrival_time = times[vIx] + self.distance_to_time(d, 8.3)
                    if arrival_time < best_option[0]:
                        best_option = (arrival_time, cIx, vIx)

            arrival_time, cIx, vIx = best_option
            if times[vIx] == self.start_time:
                to_announce.append((times[vIx], cIx, vIx))
                unassigned_vehicles[vIx] = False
                self.unassigned_customers[cIx] = False
            else:
                blocked.add(cIx)
                blocked_vehicles.add(vIx)

            travel_dist = travel_distance_m(self.scenario.customers[cIx])
            times[vIx] = arrival_time + self.distance_to_time(travel_dist, 8.3)

        ap_update = {}
        for timestamp, cIx, vIx in to_announce:
            ap_update[self.scenario.vehicles[vIx].id] = (timestamp, cIx)
            self.sent_messages += 1
        self.ap.update(ap_update)

    def compute_assignment(self, moved_vehicle: Vehicle):
        best_option = (self.start_time + 173345345, -1, -1)
        for cIx, customer in enumerate(self.scenario.customers):
            if not self.unassigned_customers[cIx]:
                continue
            available_time, posX, posY = self.av_veh[moved_vehicle.id]
            d = customer_reach_distance_m(posX, posY, customer)
            arrival_time = available_time + self.distance_to_time(d, 8.3)
            if arrival_time < best_option[0]:
                best_option = (available_time, cIx, moved_vehicle.id)

        if best_option[1] == -1:
            return
        available_time, cIx, vId = best_option
        self.unassigned_customers[cIx] = False
        self.sent_messages += 1
        self.ap.replace(vId, available_time, cIx)

    def refinement_loop(self):
        self.compute_initial_assignment()
        while self.sent_messages < len(self.scenario.customers):
            try:
                moved_vehicle = self.state_queue.get()  # blocking call -> wait for updates
                self.process_update(moved_vehicle)
            except queue.Empty:
                return

    def distance_to_time(self, dst: float, speed: float):
        return dst / speed * self.sim_speed


    def process_update(self, moved_vehicle: Vehicle):
        # we now know how fast the vehicle is actually moving
        vId = moved_vehicle.id

        customer = None
        for c in self.scenario.customers:
            if c.id == moved_vehicle.customer_id:
                customer = c
                break

        tv_dist = travel_distance_m(customer)
        app_dist = approach_distance_m(moved_vehicle, customer)
        speed = moved_vehicle.vehicle_speed
        next_timestep = self.av_veh[vId][0] + self.distance_to_time(app_dist, speed) + self.distance_to_time(tv_dist, speed)

        # the vehicle will again become available at this time in this place:
        self.av_veh[vId] = (next_timestep, customer.destination_x, customer.destination_y)

        if any(self.unassigned_customers):
            self.compute_assignment(moved_vehicle)


        # fix AP
        # ls = self.schedule.get()[vId]
        # current_ix = ls.index(asm.cIx)
        # if current_ix != len(ls) - 1:
        #     next_customer = ls[current_ix + 1]
        #     self.ap.replace(vId, next_timestep, next_customer)

        # self.local_optimize(moved_vehicle)

    def time_to_reach(self, vehicle: Vehicle, customer: Customer):
        base_time, posX, posY = self.av_veh[vehicle.id]
        return base_time + self.distance_to_time(customer_reach_distance_m(posX, posY, customer), vehicle.vehicle_speed)

    def swap_gain(self, v1: Vehicle, v2: Vehicle, c1: Customer, c2: Customer):
        ttr = self.time_to_reach(v1, c2)
        ttr_other = self.time_to_reach(v1, c2)

        ttr = self.time_to_reach(v2, c1)
        ttr_other = self.time_to_reach(v2, c1)

    def local_optimize(self, moved_vehicle: Vehicle):
        # try swapping routes
        local_schedule = self.schedule.get()[moved_vehicle.id]  # todo make schedule a dict
        if len(local_schedule) < 2:
            return  # nothing to optimize here

        next_stop = local_schedule[1]
        for other in self.scenario.vehicles:
            if other.id == moved_vehicle.id:
                continue

            other_schedule = self.schedule.get()[other.id]
            if len(other_schedule) < 2:
                continue  # nothing to optimize here

            other_followup = other_schedule[1]

            # Check if it helps to swap tours:


class Announcer(BaseStrategy):
    arv: Arvernus
    announcement_plan: AnnouncementPlan
    start_time: float
    sim_speed: float
    num_sent: int

    def __init__(self, client: Client, scenario: Scenario) -> None:
        super().__init__(client, scenario)

    @override
    def run(self, speed=0.2):
        self.initialize()
        self.announcement_plan = AnnouncementPlan()
        self.arv = Arvernus(self.state_queue, self.announcement_plan)

        self.num_sent = 0
        self.sim_speed = speed
        self.start_time = time()
        self.arv.init_scenario(self.scenario, self.start_time, speed)

        self.refinement_thread = threading.Thread(target=self.arv.refinement_loop)
        self.refinement_thread.start()  # TODO: join

        super().run(speed)

    @override
    def running(self) -> bool:
        return self.num_sent < len(self.scenario.customers)

    @override
    def strategy_loop(self):
        last_update = 0
        while self.running():
            ap = self.announcement_plan.get()

            if not ap:
                continue

            current_time = time()  # self.start_time + (time() - self.start_time) * self.sim_speed

            pending_updates = []
            for vId, (tm, cIx) in ap.items():
                logging.info(f"tm: {tm - self.start_time}, current_time: {current_time - self.start_time}, last_time: {last_update - self.start_time}")
                if tm <= current_time and tm > last_update:
                    pending_updates.append(VehicleUpdate(vId, self.scenario.customers[cIx].id))

            if len(pending_updates) > 0:
                update = UpdateScenario(pending_updates)
                self.update_queue.put(update)
                last_update = current_time

            sleep(1.0)

        self.refinement_thread.join()
