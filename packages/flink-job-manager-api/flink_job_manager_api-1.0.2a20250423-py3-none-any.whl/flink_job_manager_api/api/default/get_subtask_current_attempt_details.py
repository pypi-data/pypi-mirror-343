from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.subtask_execution_attempt_details_info import SubtaskExecutionAttemptDetailsInfo
from ...types import Response


def _get_kwargs(
    jobid: str,
    vertexid: str,
    subtaskindex: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{jobid}/vertices/{vertexid}/subtasks/{subtaskindex}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SubtaskExecutionAttemptDetailsInfo]:
    if response.status_code == 200:
        response_200 = SubtaskExecutionAttemptDetailsInfo.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SubtaskExecutionAttemptDetailsInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    jobid: str,
    vertexid: str,
    subtaskindex: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[SubtaskExecutionAttemptDetailsInfo]:
    """Returns details of the current or latest execution attempt of a subtask.

    Args:
        jobid (str):
        vertexid (str):
        subtaskindex (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubtaskExecutionAttemptDetailsInfo]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        vertexid=vertexid,
        subtaskindex=subtaskindex,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    jobid: str,
    vertexid: str,
    subtaskindex: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[SubtaskExecutionAttemptDetailsInfo]:
    """Returns details of the current or latest execution attempt of a subtask.

    Args:
        jobid (str):
        vertexid (str):
        subtaskindex (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubtaskExecutionAttemptDetailsInfo
    """

    return sync_detailed(
        jobid=jobid,
        vertexid=vertexid,
        subtaskindex=subtaskindex,
        client=client,
    ).parsed


async def asyncio_detailed(
    jobid: str,
    vertexid: str,
    subtaskindex: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[SubtaskExecutionAttemptDetailsInfo]:
    """Returns details of the current or latest execution attempt of a subtask.

    Args:
        jobid (str):
        vertexid (str):
        subtaskindex (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SubtaskExecutionAttemptDetailsInfo]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        vertexid=vertexid,
        subtaskindex=subtaskindex,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    jobid: str,
    vertexid: str,
    subtaskindex: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[SubtaskExecutionAttemptDetailsInfo]:
    """Returns details of the current or latest execution attempt of a subtask.

    Args:
        jobid (str):
        vertexid (str):
        subtaskindex (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SubtaskExecutionAttemptDetailsInfo
    """

    return (
        await asyncio_detailed(
            jobid=jobid,
            vertexid=vertexid,
            subtaskindex=subtaskindex,
            client=client,
        )
    ).parsed
