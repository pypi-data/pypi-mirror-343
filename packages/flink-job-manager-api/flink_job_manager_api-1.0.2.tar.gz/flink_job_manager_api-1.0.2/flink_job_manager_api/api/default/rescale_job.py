from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.trigger_response import TriggerResponse
from ...types import UNSET, Response


def _get_kwargs(
    jobid: str,
    *,
    parallelism: int,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["parallelism"] = parallelism

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/jobs/{jobid}/rescaling",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[TriggerResponse]:
    if response.status_code == 200:
        response_200 = TriggerResponse.from_dict(response.json())

        return response_200
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
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    parallelism: int,
) -> Response[TriggerResponse]:
    """Triggers the rescaling of a job. This async operation would return a 'triggerid' for further query
    identifier.

    Args:
        jobid (str):
        parallelism (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerResponse]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        parallelism=parallelism,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    parallelism: int,
) -> Optional[TriggerResponse]:
    """Triggers the rescaling of a job. This async operation would return a 'triggerid' for further query
    identifier.

    Args:
        jobid (str):
        parallelism (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerResponse
    """

    return sync_detailed(
        jobid=jobid,
        client=client,
        parallelism=parallelism,
    ).parsed


async def asyncio_detailed(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    parallelism: int,
) -> Response[TriggerResponse]:
    """Triggers the rescaling of a job. This async operation would return a 'triggerid' for further query
    identifier.

    Args:
        jobid (str):
        parallelism (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerResponse]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        parallelism=parallelism,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    parallelism: int,
) -> Optional[TriggerResponse]:
    """Triggers the rescaling of a job. This async operation would return a 'triggerid' for further query
    identifier.

    Args:
        jobid (str):
        parallelism (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerResponse
    """

    return (
        await asyncio_detailed(
            jobid=jobid,
            client=client,
            parallelism=parallelism,
        )
    ).parsed
