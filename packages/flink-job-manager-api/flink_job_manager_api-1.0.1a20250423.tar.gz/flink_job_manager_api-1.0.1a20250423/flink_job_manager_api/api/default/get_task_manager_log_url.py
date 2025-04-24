from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.log_url_response import LogUrlResponse
from ...types import Response


def _get_kwargs(
    jobid: str,
    taskmanagerid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{jobid}/taskmanagers/{taskmanagerid}/log-url",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[LogUrlResponse]:
    if response.status_code == 200:
        response_200 = LogUrlResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[LogUrlResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    jobid: str,
    taskmanagerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[LogUrlResponse]:
    """Returns the log url of jobmanager of a specific job.

    Args:
        jobid (str):
        taskmanagerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LogUrlResponse]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        taskmanagerid=taskmanagerid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    jobid: str,
    taskmanagerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[LogUrlResponse]:
    """Returns the log url of jobmanager of a specific job.

    Args:
        jobid (str):
        taskmanagerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LogUrlResponse
    """

    return sync_detailed(
        jobid=jobid,
        taskmanagerid=taskmanagerid,
        client=client,
    ).parsed


async def asyncio_detailed(
    jobid: str,
    taskmanagerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[LogUrlResponse]:
    """Returns the log url of jobmanager of a specific job.

    Args:
        jobid (str):
        taskmanagerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LogUrlResponse]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        taskmanagerid=taskmanagerid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    jobid: str,
    taskmanagerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[LogUrlResponse]:
    """Returns the log url of jobmanager of a specific job.

    Args:
        jobid (str):
        taskmanagerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LogUrlResponse
    """

    return (
        await asyncio_detailed(
            jobid=jobid,
            taskmanagerid=taskmanagerid,
            client=client,
        )
    ).parsed
