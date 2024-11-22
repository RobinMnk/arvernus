from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from .... import errors
from ....client import AuthenticatedClient, Client
from ...models.scenario_dto import ScenarioDTO
from ....types import UNSET, Response, Unset


def _get_kwargs(
    *,
    number_of_vehicles: Union[Unset, int] = UNSET,
    number_of_customers: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["numberOfVehicles"] = number_of_vehicles

    params["numberOfCustomers"] = number_of_customers

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/scenario/create",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ScenarioDTO]:
    if response.status_code == 200:
        response_200 = ScenarioDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ScenarioDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    number_of_vehicles: Union[Unset, int] = UNSET,
    number_of_customers: Union[Unset, int] = UNSET,
) -> Response[ScenarioDTO]:
    """Initialize a scenario

     Initialize a random scenario

    Args:
        number_of_vehicles (Union[Unset, int]):
        number_of_customers (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScenarioDTO]
    """

    kwargs = _get_kwargs(
        number_of_vehicles=number_of_vehicles,
        number_of_customers=number_of_customers,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    number_of_vehicles: Union[Unset, int] = UNSET,
    number_of_customers: Union[Unset, int] = UNSET,
) -> Optional[ScenarioDTO]:
    """Initialize a scenario

     Initialize a random scenario

    Args:
        number_of_vehicles (Union[Unset, int]):
        number_of_customers (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScenarioDTO
    """

    return sync_detailed(
        client=client,
        number_of_vehicles=number_of_vehicles,
        number_of_customers=number_of_customers,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    number_of_vehicles: Union[Unset, int] = UNSET,
    number_of_customers: Union[Unset, int] = UNSET,
) -> Response[ScenarioDTO]:
    """Initialize a scenario

     Initialize a random scenario

    Args:
        number_of_vehicles (Union[Unset, int]):
        number_of_customers (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScenarioDTO]
    """

    kwargs = _get_kwargs(
        number_of_vehicles=number_of_vehicles,
        number_of_customers=number_of_customers,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    number_of_vehicles: Union[Unset, int] = UNSET,
    number_of_customers: Union[Unset, int] = UNSET,
) -> Optional[ScenarioDTO]:
    """Initialize a scenario

     Initialize a random scenario

    Args:
        number_of_vehicles (Union[Unset, int]):
        number_of_customers (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScenarioDTO
    """

    return (
        await asyncio_detailed(
            client=client,
            number_of_vehicles=number_of_vehicles,
            number_of_customers=number_of_customers,
        )
    ).parsed
