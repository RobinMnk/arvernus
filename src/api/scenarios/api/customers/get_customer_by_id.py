from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from uuid import UUID

import httpx

from .... import errors
from ....client import AuthenticatedClient, Client
from ...models.customer_dto import CustomerDTO
from ...models.response_message import ResponseMessage
from ....types import Response


def _get_kwargs(
    customer_id: UUID,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/customers/{customer_id}",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[CustomerDTO, ResponseMessage]]:
    if response.status_code == 200:
        response_200 = CustomerDTO.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = ResponseMessage.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[CustomerDTO, ResponseMessage]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    customer_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[CustomerDTO, ResponseMessage]]:
    """Get a customer

     Get a customer with the given id

    Args:
        customer_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CustomerDTO, ResponseMessage]]
    """

    kwargs = _get_kwargs(
        customer_id=customer_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    customer_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[CustomerDTO, ResponseMessage]]:
    """Get a customer

     Get a customer with the given id

    Args:
        customer_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CustomerDTO, ResponseMessage]
    """

    return sync_detailed(
        customer_id=customer_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    customer_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[CustomerDTO, ResponseMessage]]:
    """Get a customer

     Get a customer with the given id

    Args:
        customer_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CustomerDTO, ResponseMessage]]
    """

    kwargs = _get_kwargs(
        customer_id=customer_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    customer_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[CustomerDTO, ResponseMessage]]:
    """Get a customer

     Get a customer with the given id

    Args:
        customer_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CustomerDTO, ResponseMessage]
    """

    return (
        await asyncio_detailed(
            customer_id=customer_id,
            client=client,
        )
    ).parsed
