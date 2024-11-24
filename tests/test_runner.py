from http import HTTPStatus
import random
from uuid import UUID
import logging

from api.client import Client
from api.runner.api.runner import post_launch_scenario
from api.runner.api.scenarios import post_initialize_scenario
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
    vehicles = [
        Vehicle(str(UUID(int=0)), random_x_coord(), random_y_coord(), True),
        Vehicle(str(UUID(int=1)), random_x_coord(), random_y_coord(), True),
    ]
    customers = [
        Customer(str(UUID(int=0)), random_x_coord(), random_y_coord(), random_x_coord(), random_y_coord(), True),
        Customer(str(UUID(int=1)), random_x_coord(), random_y_coord(), random_x_coord(), random_y_coord(), True),
        Customer(str(UUID(int=2)), random_x_coord(), random_y_coord(), random_x_coord(), random_y_coord(), True),
    ]
    scenario = Scenario(str(UUID(int=0)), UNSET, UNSET, UNSET, vehicles, customers)

    # strategy = RandomStrategy(client, scenario)
    # strategy = MatchingStrategy(client, scenario)
    strategy = Announcer(client, scenario)

    strategy.run(speed=0.002)
