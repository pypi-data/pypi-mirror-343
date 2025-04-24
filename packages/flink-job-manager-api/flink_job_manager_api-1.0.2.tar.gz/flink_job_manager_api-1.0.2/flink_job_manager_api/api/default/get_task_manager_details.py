from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.task_manager_details_info import TaskManagerDetailsInfo
from ...types import Response


def _get_kwargs(
    taskmanagerid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/taskmanagers/{taskmanagerid}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[TaskManagerDetailsInfo]:
    if response.status_code == 200:
        response_200 = TaskManagerDetailsInfo.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[TaskManagerDetailsInfo]:
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
) -> Response[TaskManagerDetailsInfo]:
    """Returns details for a task manager.

    Args:
        taskmanagerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TaskManagerDetailsInfo]
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
) -> Optional[TaskManagerDetailsInfo]:
    """Returns details for a task manager.

    Args:
        taskmanagerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TaskManagerDetailsInfo
    """

    return sync_detailed(
        taskmanagerid=taskmanagerid,
        client=client,
    ).parsed


async def asyncio_detailed(
    taskmanagerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[TaskManagerDetailsInfo]:
    """Returns details for a task manager.

    Args:
        taskmanagerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TaskManagerDetailsInfo]
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
) -> Optional[TaskManagerDetailsInfo]:
    """Returns details for a task manager.

    Args:
        taskmanagerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TaskManagerDetailsInfo
    """

    return (
        await asyncio_detailed(
            taskmanagerid=taskmanagerid,
            client=client,
        )
    ).parsed
