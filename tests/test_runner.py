from datetime import datetime
from http import HTTPStatus
import json
import random
from uuid import UUID
import logging

from api.client import Client
from api.runner.api.runner import post_launch_scenario
from api.runner.api.scenarios import get_get_scenario, post_initialize_scenario
from api.runner.models.customer import Customer
from api.runner.models.scenario import Scenario
from api.runner.models.vehicle import Vehicle
from api.types import UNSET
from arvernus.matching import MatchingStrategy
from arvernus.schedule import Announcer
from arvernus.strategy.base_strategy import RandomStrategy

client = Client(base_url="http://localhost:8090")


LOGGER = logging.getLogger("module")
LOGGER.propagate = True


def random_x_coord():
    return 48 + random.random()


def random_y_coord():
    return 11 + random.random()


def test_run():
    scenario = generate_benchmark()

    strategy = MatchingStrategy(client, scenario)
    # strategy = RandomStrategy(client, scenario)

    strategy.initialize()
    strategy.run(speed=0.02)

    response = get_get_scenario.sync_detailed(client=client, scenario_id=scenario.id)
    scenario = Scenario.from_response(response)

    start = datetime.fromisoformat(scenario.start_time)
    end = datetime.fromisoformat(scenario.end_time)

    total_distance = sum([vehicle.distance_travelled for vehicle in scenario.vehicles])

    logging.info(f"Took {end - start}s and {total_distance} distance")


def generate_random_scenario(num_vehicles=3, num_customers=5) -> Scenario:
    vehicles = []
    for i in range(num_vehicles):
        vehicles.append(
            Vehicle(str(UUID(int=i)), random_x_coord(), random_y_coord(), True),
        )

    customers = []
    for i in range(num_customers):
        customers.append(
            Customer(str(UUID(int=i)), random_x_coord(), random_y_coord(), random_x_coord(), random_y_coord(), True),
        )
    scenario = Scenario(str(UUID(int=0)), UNSET, UNSET, UNSET, vehicles, customers)
    return scenario


def generate_benchmark():
    return Scenario.from_dict(json.loads(BENCHMARK))


BENCHMARK = """
{
"id": "00000000-0000-0000-0000-000000000000",
"startTime": null,
"endTime": null,
"status": "CREATED",
"vehicles": [
{
"id": "78de0937-7d0e-45fe-b095-4742942ca314",
"coordX": 48.160213,
"coordY": 11.556228,
"isAvailable": true,
"vehicleSpeed": null,
"customerId": null,
"remainingTravelTime": null,
"distanceTravelled": null,
"activeTime": null,
"numberOfTrips": null
},
{
"id": "e41d475f-f7c7-4581-9911-4e86be08238e",
"coordX": 48.130985,
"coordY": 11.620369,
"isAvailable": true,
"vehicleSpeed": null,
"customerId": null,
"remainingTravelTime": null,
"distanceTravelled": null,
"activeTime": null,
"numberOfTrips": null
},
{
"id": "7f951211-fb17-47de-83bd-06277ba6de0e",
"coordX": 48.152977,
"coordY": 11.62258,
"isAvailable": true,
"vehicleSpeed": null,
"customerId": null,
"remainingTravelTime": null,
"distanceTravelled": null,
"activeTime": null,
"numberOfTrips": null
},
{
"id": "47018d25-e1dd-469d-91b5-de92e6a22022",
"coordX": 48.152607,
"coordY": 11.583268,
"isAvailable": true,
"vehicleSpeed": null,
"customerId": null,
"remainingTravelTime": null,
"distanceTravelled": null,
"activeTime": null,
"numberOfTrips": null
},
{
"id": "a2d0eb84-2d2d-499b-b68c-323d1aca6961",
"coordX": 48.116234,
"coordY": 11.630238,
"isAvailable": true,
"vehicleSpeed": null,
"customerId": null,
"remainingTravelTime": null,
"distanceTravelled": null,
"activeTime": null,
"numberOfTrips": null
},
{
"id": "c5a0ac0f-908f-42a1-9260-ff479a3a8848",
"coordX": 48.130486,
"coordY": 11.5681,
"isAvailable": true,
"vehicleSpeed": null,
"customerId": null,
"remainingTravelTime": null,
"distanceTravelled": null,
"activeTime": null,
"numberOfTrips": null
},
{
"id": "1527c0e5-48de-442e-9f3a-222b387b3b07",
"coordX": 48.164753,
"coordY": 11.617963,
"isAvailable": true,
"vehicleSpeed": null,
"customerId": null,
"remainingTravelTime": null,
"distanceTravelled": null,
"activeTime": null,
"numberOfTrips": null
},
{
"id": "1d0705ae-e789-48f9-ac5f-1d8edbf80114",
"coordX": 48.158836,
"coordY": 11.609071,
"isAvailable": true,
"vehicleSpeed": null,
"customerId": null,
"remainingTravelTime": null,
"distanceTravelled": null,
"activeTime": null,
"numberOfTrips": null
},
{
"id": "b5f45500-b17d-48fa-a213-508059fcf2cb",
"coordX": 48.11372,
"coordY": 11.585152,
"isAvailable": true,
"vehicleSpeed": null,
"customerId": null,
"remainingTravelTime": null,
"distanceTravelled": null,
"activeTime": null,
"numberOfTrips": null
},
{
"id": "d7c86ef9-3bb6-464e-a312-dd8d3ffef2de",
"coordX": 48.146328,
"coordY": 11.52796,
"isAvailable": true,
"vehicleSpeed": null,
"customerId": null,
"remainingTravelTime": null,
"distanceTravelled": null,
"activeTime": null,
"numberOfTrips": null
}
],
"customers": [
{
"id": "dbc8dae8-2730-4bc2-97a1-6b0b6f4de6ee",
"coordX": 48.14119,
"coordY": 11.559336,
"destinationX": 48.162136,
"destinationY": 11.54945,
"awaitingService": true
},
{
"id": "a8709f15-a4f5-49b7-953c-ede05cf3823b",
"coordX": 48.119617,
"coordY": 11.5751915,
"destinationX": 48.120686,
"destinationY": 11.510352,
"awaitingService": true
},
{
"id": "052cd065-af5e-4d1e-95f9-fd869cbc1afc",
"coordX": 48.128933,
"coordY": 11.516576,
"destinationX": 48.13982,
"destinationY": 11.582378,
"awaitingService": true
},
{
"id": "c1ffefcf-e6d2-4ea3-9b71-227bebad2ff8",
"coordX": 48.11352,
"coordY": 11.5865965,
"destinationX": 48.12133,
"destinationY": 11.591613,
"awaitingService": true
},
{
"id": "3198b70a-b305-4784-8020-4b3b5b0ff22b",
"coordX": 48.137074,
"coordY": 11.631897,
"destinationX": 48.116337,
"destinationY": 11.545822,
"awaitingService": true
},
{
"id": "fb96cd25-dea5-4b67-9892-408c492a9d6f",
"coordX": 48.164276,
"coordY": 11.635528,
"destinationX": 48.132225,
"destinationY": 11.59809,
"awaitingService": true
},
{
"id": "839ea817-a3a3-4295-a536-0f18866038e5",
"coordX": 48.11685,
"coordY": 11.554019,
"destinationX": 48.129887,
"destinationY": 11.645615,
"awaitingService": true
},
{
"id": "741057ee-27b3-4ce5-bbbf-9552a59cffb3",
"coordX": 48.114174,
"coordY": 11.630232,
"destinationX": 48.116673,
"destinationY": 11.525897,
"awaitingService": true
},
{
"id": "a8e86bd1-28ef-4898-89bd-c17400090336",
"coordX": 48.118286,
"coordY": 11.538289,
"destinationX": 48.160316,
"destinationY": 11.515464,
"awaitingService": true
},
{
"id": "60db144c-2251-4c5e-b894-37e332c15a92",
"coordX": 48.143456,
"coordY": 11.530519,
"destinationX": 48.156998,
"destinationY": 11.523938,
"awaitingService": true
},
{
"id": "5d88164d-2a30-4ac0-8f40-bbcaa62bdf56",
"coordX": 48.14927,
"coordY": 11.575575,
"destinationX": 48.13192,
"destinationY": 11.58971,
"awaitingService": true
},
{
"id": "b7b5779a-c76e-48b4-ade4-10d8bebbbb47",
"coordX": 48.128036,
"coordY": 11.536889,
"destinationX": 48.146183,
"destinationY": 11.57223,
"awaitingService": true
},
{
"id": "d42fc44e-fa61-4fdd-a9a2-f2b1998b94a8",
"coordX": 48.145992,
"coordY": 11.637683,
"destinationX": 48.115417,
"destinationY": 11.568507,
"awaitingService": true
},
{
"id": "885c3c6b-4a7c-44b8-a1ae-78774521c9ab",
"coordX": 48.13389,
"coordY": 11.590477,
"destinationX": 48.130573,
"destinationY": 11.576796,
"awaitingService": true
},
{
"id": "789bea35-66aa-404a-a6cf-b2c9e5730a06",
"coordX": 48.12253,
"coordY": 11.645378,
"destinationX": 48.12168,
"destinationY": 11.555196,
"awaitingService": true
},
{
"id": "ecafe513-9028-4c54-9c32-906818d6a3eb",
"coordX": 48.159622,
"coordY": 11.527176,
"destinationX": 48.12802,
"destinationY": 11.612381,
"awaitingService": true
},
{
"id": "dadf32f6-a96d-4158-926e-05cd0ec8d817",
"coordX": 48.11574,
"coordY": 11.6032915,
"destinationX": 48.124783,
"destinationY": 11.570208,
"awaitingService": true
},
{
"id": "26a35cd1-5e04-43e9-a9df-4337f6cba139",
"coordX": 48.151295,
"coordY": 11.583676,
"destinationX": 48.11926,
"destinationY": 11.598211,
"awaitingService": true
},
{
"id": "2b5ac4ef-ab1f-4dfb-8b58-f837903907c5",
"coordX": 48.11973,
"coordY": 11.569333,
"destinationX": 48.126293,
"destinationY": 11.5253525,
"awaitingService": true
},
{
"id": "e68c520d-c72b-428e-9d0e-ee7ab94099a3",
"coordX": 48.148136,
"coordY": 11.52848,
"destinationX": 48.15456,
"destinationY": 11.610386,
"awaitingService": true
}
]
}
"""
