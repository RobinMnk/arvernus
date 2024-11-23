from http import HTTPStatus
from uuid import UUID
from flask import Flask, make_response, request
from api.client import Client
from api.runner.api.scenarios import get_get_scenario
from api.runner.models.scenario import Scenario
from api.scenarios.api import scenario
from api.scenarios.api.scenario import get_scenario_by_id
from arvernus.strategy.base_strategy import RandomStrategy

app = Flask(__name__)

scenarios_client = Client(base_url="http://localhost:8080")
runner_client = Client(base_url="http://localhost:8090")


@app.route("/run/<scenario_id>", methods=["POST"])
def run(scenario_id: UUID):
    scenario_dto = get_scenario_by_id.sync(client=scenarios_client, scenario_id=scenario_id)
    if not scenario_dto:
        return make_response("", 404)

    scenario = Scenario.from_dto(scenario_dto)
    speed = float(request.form["speed"])

    strategy = RandomStrategy(runner_client, scenario)

    strategy.initialize()
    strategy.run(speed=speed)  # TODO add speed

    scenario = None

    return make_response("", 200)


@app.route("/scenario/<scenario_id>", methods=["get"])
def scenario(scenario_id: str):
    response = get_get_scenario.sync_detailed(client=runner_client, scenario_id=scenario_id)
    scenario = Scenario.from_response(response)
    return scenario.to_dict()
