from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import httpx

from .... import errors
from ....client import AuthenticatedClient, Client
from ...models.response_message import ResponseMessage
from ...models.standard_magenta_vehicle_dto import StandardMagentaVehicleDTO
from ....types import Response


def _get_kwargs(
    scenario_id: UUID,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/scenarios/{scenario_id}/vehicles",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[List["StandardMagentaVehicleDTO"], ResponseMessage]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = StandardMagentaVehicleDTO.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 404:
        response_404 = ResponseMessage.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[List["StandardMagentaVehicleDTO"], ResponseMessage]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scenario_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[List["StandardMagentaVehicleDTO"], ResponseMessage]]:
    """Get all vehicles for a scenario

     Get all vehicles for a scenario with the given id

    Args:
        scenario_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['StandardMagentaVehicleDTO'], ResponseMessage]]
    """

    kwargs = _get_kwargs(
        scenario_id=scenario_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    scenario_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[List["StandardMagentaVehicleDTO"], ResponseMessage]]:
    """Get all vehicles for a scenario

     Get all vehicles for a scenario with the given id

    Args:
        scenario_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['StandardMagentaVehicleDTO'], ResponseMessage]
    """

    return sync_detailed(
        scenario_id=scenario_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    scenario_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[List["StandardMagentaVehicleDTO"], ResponseMessage]]:
    """Get all vehicles for a scenario

     Get all vehicles for a scenario with the given id

    Args:
        scenario_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['StandardMagentaVehicleDTO'], ResponseMessage]]
    """

    kwargs = _get_kwargs(
        scenario_id=scenario_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scenario_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[List["StandardMagentaVehicleDTO"], ResponseMessage]]:
    """Get all vehicles for a scenario

     Get all vehicles for a scenario with the given id

    Args:
        scenario_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['StandardMagentaVehicleDTO'], ResponseMessage]
    """

    return (
        await asyncio_detailed(
            scenario_id=scenario_id,
            client=client,
        )
    ).parsed
