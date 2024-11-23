from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from uuid import UUID

import httpx

from .... import errors
from ....client import AuthenticatedClient, Client
from ...models.scenario_metadata_dto import ScenarioMetadataDTO
from ....types import Response


def _get_kwargs(
    scenario_id: UUID,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/scenario/{scenario_id}/metadata",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ScenarioMetadataDTO]:
    if response.status_code == 200:
        response_200 = ScenarioMetadataDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ScenarioMetadataDTO]:
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
) -> Response[ScenarioMetadataDTO]:
    """Get scenario metadata

     Get the metadata of a scenario

    Args:
        scenario_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScenarioMetadataDTO]
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
) -> Optional[ScenarioMetadataDTO]:
    """Get scenario metadata

     Get the metadata of a scenario

    Args:
        scenario_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScenarioMetadataDTO
    """

    return sync_detailed(
        scenario_id=scenario_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    scenario_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ScenarioMetadataDTO]:
    """Get scenario metadata

     Get the metadata of a scenario

    Args:
        scenario_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScenarioMetadataDTO]
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
) -> Optional[ScenarioMetadataDTO]:
    """Get scenario metadata

     Get the metadata of a scenario

    Args:
        scenario_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScenarioMetadataDTO
    """

    return (
        await asyncio_detailed(
            scenario_id=scenario_id,
            client=client,
        )
    ).parsed