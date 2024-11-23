from http import HTTPStatus
import random
from uuid import UUID

from api.client import Client
from api.runner.api.runner import post_launch_scenario
from api.runner.api.scenarios import post_initialize_scenario
from api.runner.models.customer import Customer
from api.runner.models.scenario import Scenario
from api.runner.models.vehicle import Vehicle
from api.types import UNSET

client = Client(base_url="http://localhost:8090")


def random_x_coord():
    return 48 + random.random()


def random_y_coord():
    return 11 + random.random()


def test_run():
    vehicles = [
        Vehicle(str(UUID(int=0)), random_x_coord(), random_y_coord()),
        Vehicle(str(UUID(int=1)), random_x_coord(), random_y_coord()),
    ]
    customers = [
        Customer(str(UUID(int=0)), random_x_coord(), random_y_coord(), random_x_coord(), random_y_coord(), True),
        Customer(str(UUID(int=1)), random_x_coord(), random_y_coord(), random_x_coord(), random_y_coord(), True),
        Customer(str(UUID(int=2)), random_x_coord(), random_y_coord(), random_x_coord(), random_y_coord(), True),
    ]
    scenario = Scenario(str(UUID(int=0)), UNSET, UNSET, "CREATED", vehicles, customers)

    initialize = post_initialize_scenario.sync_detailed(client=client, body=scenario)
    assert initialize.status_code == HTTPStatus.OK

    launch = post_launch_scenario.sync_detailed(client=client, speed=0.2, scenario_id=scenario.id)
    assert launch.status_code == HTTPStatus.OK
