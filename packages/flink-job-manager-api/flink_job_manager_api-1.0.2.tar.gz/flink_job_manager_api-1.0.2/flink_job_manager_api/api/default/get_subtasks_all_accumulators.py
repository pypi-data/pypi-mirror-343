from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.subtasks_all_accumulators_info import SubtasksAllAccumulatorsInfo
from ...types import Response


def _get_kwargs(
    jobid: str,
    vertexid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{jobid}/vertices/{vertexid}/subtasks/accumulators",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SubtasksAllAccumulatorsInfo]:
    if response.status_code == 200:
        response_200 = SubtasksAllAccumulatorsInfo.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SubtasksAllAccumulatorsInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    jobid: str,
    vertexid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[SubtasksAllAccumulatorsInfo]:
    """Returns all user-defined accumulators for all subtasks of a task.

    Args:
        jobid (str):
        vertexid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubtasksAllAccumulatorsInfo]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        vertexid=vertexid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    jobid: str,
    vertexid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[SubtasksAllAccumulatorsInfo]:
    """Returns all user-defined accumulators for all subtasks of a task.

    Args:
        jobid (str):
        vertexid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubtasksAllAccumulatorsInfo
    """

    return sync_detailed(
        jobid=jobid,
        vertexid=vertexid,
        client=client,
    ).parsed


async def asyncio_detailed(
    jobid: str,
    vertexid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[SubtasksAllAccumulatorsInfo]:
    """Returns all user-defined accumulators for all subtasks of a task.

    Args:
        jobid (str):
        vertexid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubtasksAllAccumulatorsInfo]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        vertexid=vertexid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    jobid: str,
    vertexid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[SubtasksAllAccumulatorsInfo]:
    """Returns all user-defined accumulators for all subtasks of a task.

    Args:
        jobid (str):
        vertexid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubtasksAllAccumulatorsInfo
    """

    return (
        await asyncio_detailed(
            jobid=jobid,
            vertexid=vertexid,
            client=client,
        )
    ).parsed
