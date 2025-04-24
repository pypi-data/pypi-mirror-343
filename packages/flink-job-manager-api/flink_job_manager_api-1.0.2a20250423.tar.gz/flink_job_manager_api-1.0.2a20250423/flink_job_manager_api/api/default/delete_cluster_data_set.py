from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.trigger_response import TriggerResponse
from ...types import Response


def _get_kwargs(
    datasetid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/datasets/{datasetid}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[TriggerResponse]:
    if response.status_code == 202:
        response_202 = TriggerResponse.from_dict(response.json())

        return response_202
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[TriggerResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    datasetid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[TriggerResponse]:
    """Triggers the deletion of a cluster data set. This async operation would return a 'triggerid' for
    further query identifier.

    Args:
        datasetid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerResponse]
    """

    kwargs = _get_kwargs(
        datasetid=datasetid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    datasetid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[TriggerResponse]:
    """Triggers the deletion of a cluster data set. This async operation would return a 'triggerid' for
    further query identifier.

    Args:
        datasetid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerResponse
    """

    return sync_detailed(
        datasetid=datasetid,
        client=client,
    ).parsed


async def asyncio_detailed(
    datasetid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[TriggerResponse]:
    """Triggers the deletion of a cluster data set. This async operation would return a 'triggerid' for
    further query identifier.

    Args:
        datasetid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerResponse]
    """

    kwargs = _get_kwargs(
        datasetid=datasetid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    datasetid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[TriggerResponse]:
    """Triggers the deletion of a cluster data set. This async operation would return a 'triggerid' for
    further query identifier.

    Args:
        datasetid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerResponse
    """

    return (
        await asyncio_detailed(
            datasetid=datasetid,
            client=client,
        )
    ).parsed
