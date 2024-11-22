from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from uuid import UUID

import httpx

from .... import errors
from ....client import AuthenticatedClient, Client
from ...models.response_message import ResponseMessage
from ...models.standard_magenta_vehicle_dto import StandardMagentaVehicleDTO
from ....types import Response


def _get_kwargs(
    vehicle_id: UUID,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/vehicles/{vehicle_id}",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[ResponseMessage, StandardMagentaVehicleDTO]]:
    if response.status_code == 200:
        response_200 = StandardMagentaVehicleDTO.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = ResponseMessage.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[ResponseMessage, StandardMagentaVehicleDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    vehicle_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[ResponseMessage, StandardMagentaVehicleDTO]]:
    """Get a vehicle

     Get a vehicle with the given id

    Args:
        vehicle_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ResponseMessage, StandardMagentaVehicleDTO]]
    """

    kwargs = _get_kwargs(
        vehicle_id=vehicle_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    vehicle_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[ResponseMessage, StandardMagentaVehicleDTO]]:
    """Get a vehicle

     Get a vehicle with the given id

    Args:
        vehicle_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ResponseMessage, StandardMagentaVehicleDTO]
    """

    return sync_detailed(
        vehicle_id=vehicle_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    vehicle_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[ResponseMessage, StandardMagentaVehicleDTO]]:
    """Get a vehicle

     Get a vehicle with the given id

    Args:
        vehicle_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ResponseMessage, StandardMagentaVehicleDTO]]
    """

    kwargs = _get_kwargs(
        vehicle_id=vehicle_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    vehicle_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[ResponseMessage, StandardMagentaVehicleDTO]]:
    """Get a vehicle

     Get a vehicle with the given id

    Args:
        vehicle_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ResponseMessage, StandardMagentaVehicleDTO]
    """

    return (
        await asyncio_detailed(
            vehicle_id=vehicle_id,
            client=client,
        )
    ).parsed
