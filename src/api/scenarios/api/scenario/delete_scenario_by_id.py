from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from uuid import UUID

import httpx

from .... import errors
from ....client import AuthenticatedClient, Client
from ...models.response_message import ResponseMessage
from ....types import Response


def _get_kwargs(
    scenario_id: UUID,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/scenarios/{scenario_id}",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ResponseMessage]:
    if response.status_code == 200:
        response_200 = ResponseMessage.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = ResponseMessage.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ResponseMessage]:
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
) -> Response[ResponseMessage]:
    """Delete a scenario

     Delete a scenario with the given id

    Args:
        scenario_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseMessage]
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
) -> Optional[ResponseMessage]:
    """Delete a scenario

     Delete a scenario with the given id

    Args:
        scenario_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseMessage
    """

    return sync_detailed(
        scenario_id=scenario_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    scenario_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ResponseMessage]:
    """Delete a scenario

     Delete a scenario with the given id

    Args:
        scenario_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseMessage]
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
) -> Optional[ResponseMessage]:
    """Delete a scenario

     Delete a scenario with the given id

    Args:
        scenario_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseMessage
    """

    return (
        await asyncio_detailed(
            scenario_id=scenario_id,
            client=client,
        )
    ).parsed
