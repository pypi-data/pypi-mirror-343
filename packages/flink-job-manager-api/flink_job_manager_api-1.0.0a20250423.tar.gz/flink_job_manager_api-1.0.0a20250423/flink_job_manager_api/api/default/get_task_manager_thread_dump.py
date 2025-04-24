from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.thread_dump_info import ThreadDumpInfo
from ...types import Response


def _get_kwargs(
    taskmanagerid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/taskmanagers/{taskmanagerid}/thread-dump",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ThreadDumpInfo]:
    if response.status_code == 200:
        response_200 = ThreadDumpInfo.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ThreadDumpInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    taskmanagerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ThreadDumpInfo]:
    """Returns the thread dump of the requested TaskManager.

    Args:
        taskmanagerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ThreadDumpInfo]
    """

    kwargs = _get_kwargs(
        taskmanagerid=taskmanagerid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    taskmanagerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ThreadDumpInfo]:
    """Returns the thread dump of the requested TaskManager.

    Args:
        taskmanagerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ThreadDumpInfo
    """

    return sync_detailed(
        taskmanagerid=taskmanagerid,
        client=client,
    ).parsed


async def asyncio_detailed(
    taskmanagerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ThreadDumpInfo]:
    """Returns the thread dump of the requested TaskManager.

    Args:
        taskmanagerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ThreadDumpInfo]
    """

    kwargs = _get_kwargs(
        taskmanagerid=taskmanagerid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    taskmanagerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ThreadDumpInfo]:
    """Returns the thread dump of the requested TaskManager.

    Args:
        taskmanagerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ThreadDumpInfo
    """

    return (
        await asyncio_detailed(
            taskmanagerid=taskmanagerid,
            client=client,
        )
    ).parsed
