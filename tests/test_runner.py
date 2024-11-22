from typing import Optional, List
from api.client import Client
from api.runner.api.scenarios import post_initialize_scenario

client = Client(base_url="http://localhost:8090")


def test_initialize():
    body = {}
    response = post_initialize_scenario.sync_detailed(client=client, body=body)
