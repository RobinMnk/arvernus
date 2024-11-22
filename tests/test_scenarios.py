from typing import Optional, List
from api.client import Client
from api.scenarios.api.scenario import create_scenario, delete_scenario_by_id, get_all_scenarios, get_scenario_by_id
from api.scenarios.models.scenario_dto import ScenarioDTO

client = Client(base_url="http://localhost:8080")


def test_all_scenarios():
    scenarios: Optional[List[ScenarioDTO]] = get_all_scenarios.sync(client=client)
    if scenarios:
        for scenario in scenarios:
            print(scenario)


def test_scenario_crud():
    created = create_scenario.sync(client=client, number_of_vehicles=4, number_of_customers=2)
    assert created

    retrieved = get_scenario_by_id.sync(client=client, scenario_id=created.id)
    assert retrieved

    assert created == retrieved

    response = delete_scenario_by_id.sync(client=client, scenario_id=created.id)
    assert response and "status" not in response.additional_properties
