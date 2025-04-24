from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.termination_mode import TerminationMode
from ...types import UNSET, Response, Unset


def _get_kwargs(
    jobid: str,
    *,
    mode: Union[Unset, TerminationMode] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_mode: Union[Unset, str] = UNSET
    if not isinstance(mode, Unset):
        json_mode = mode.value

    params["mode"] = json_mode

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/jobs/{jobid}",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == 202:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
    mode: Union[Unset, TerminationMode] = UNSET,
) -> Response[Any]:
    """Terminates a job.

    Args:
        jobid (str):
        mode (Union[Unset, TerminationMode]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        mode=mode,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    mode: Union[Unset, TerminationMode] = UNSET,
) -> Response[Any]:
    """Terminates a job.

    Args:
        jobid (str):
        mode (Union[Unset, TerminationMode]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        mode=mode,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
