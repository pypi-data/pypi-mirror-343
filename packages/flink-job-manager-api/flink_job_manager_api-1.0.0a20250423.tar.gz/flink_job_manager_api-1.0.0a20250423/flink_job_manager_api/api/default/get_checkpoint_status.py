from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.asynchronous_operation_result import AsynchronousOperationResult
from ...types import Response


def _get_kwargs(
    jobid: str,
    triggerid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{jobid}/checkpoints/{triggerid}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AsynchronousOperationResult]:
    if response.status_code == 200:
        response_200 = AsynchronousOperationResult.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AsynchronousOperationResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    jobid: str,
    triggerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[AsynchronousOperationResult]:
    """Returns the status of a checkpoint trigger operation.

    Args:
        jobid (str):
        triggerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AsynchronousOperationResult]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        triggerid=triggerid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    jobid: str,
    triggerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[AsynchronousOperationResult]:
    """Returns the status of a checkpoint trigger operation.

    Args:
        jobid (str):
        triggerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AsynchronousOperationResult
    """

    return sync_detailed(
        jobid=jobid,
        triggerid=triggerid,
        client=client,
    ).parsed


async def asyncio_detailed(
    jobid: str,
    triggerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[AsynchronousOperationResult]:
    """Returns the status of a checkpoint trigger operation.

    Args:
        jobid (str):
        triggerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AsynchronousOperationResult]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        triggerid=triggerid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    jobid: str,
    triggerid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[AsynchronousOperationResult]:
    """Returns the status of a checkpoint trigger operation.

    Args:
        jobid (str):
        triggerid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AsynchronousOperationResult
    """

    return (
        await asyncio_detailed(
            jobid=jobid,
            triggerid=triggerid,
            client=client,
        )
    ).parsed
