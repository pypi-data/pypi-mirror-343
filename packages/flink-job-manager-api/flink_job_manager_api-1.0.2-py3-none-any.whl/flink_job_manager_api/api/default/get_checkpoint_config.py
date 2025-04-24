from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.checkpoint_config_info import CheckpointConfigInfo
from ...types import Response


def _get_kwargs(
    jobid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{jobid}/checkpoints/config",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CheckpointConfigInfo]:
    if response.status_code == 200:
        response_200 = CheckpointConfigInfo.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CheckpointConfigInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[CheckpointConfigInfo]:
    """Returns the checkpointing configuration.

    Args:
        jobid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckpointConfigInfo]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[CheckpointConfigInfo]:
    """Returns the checkpointing configuration.

    Args:
        jobid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckpointConfigInfo
    """

    return sync_detailed(
        jobid=jobid,
        client=client,
    ).parsed


async def asyncio_detailed(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[CheckpointConfigInfo]:
    """Returns the checkpointing configuration.

    Args:
        jobid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckpointConfigInfo]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[CheckpointConfigInfo]:
    """Returns the checkpointing configuration.

    Args:
        jobid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckpointConfigInfo
    """

    return (
        await asyncio_detailed(
            jobid=jobid,
            client=client,
        )
    ).parsed
