from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.metric_collection_response_body import MetricCollectionResponseBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    jobid: str,
    vertexid: str,
    subtaskindex: int,
    *,
    get: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["get"] = get

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{jobid}/vertices/{vertexid}/subtasks/{subtaskindex}/metrics",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[MetricCollectionResponseBody]:
    if response.status_code == 200:
        response_200 = MetricCollectionResponseBody.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MetricCollectionResponseBody]:
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
    get: Union[Unset, str] = UNSET,
) -> Response[MetricCollectionResponseBody]:
    """Provides access to subtask metrics.

    Args:
        jobid (str):
        vertexid (str):
        subtaskindex (int):
        get (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MetricCollectionResponseBody]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        vertexid=vertexid,
        subtaskindex=subtaskindex,
        get=get,
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
    get: Union[Unset, str] = UNSET,
) -> Optional[MetricCollectionResponseBody]:
    """Provides access to subtask metrics.

    Args:
        jobid (str):
        vertexid (str):
        subtaskindex (int):
        get (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MetricCollectionResponseBody
    """

    return sync_detailed(
        jobid=jobid,
        vertexid=vertexid,
        subtaskindex=subtaskindex,
        client=client,
        get=get,
    ).parsed


async def asyncio_detailed(
    jobid: str,
    vertexid: str,
    subtaskindex: int,
    *,
    client: Union[AuthenticatedClient, Client],
    get: Union[Unset, str] = UNSET,
) -> Response[MetricCollectionResponseBody]:
    """Provides access to subtask metrics.

    Args:
        jobid (str):
        vertexid (str):
        subtaskindex (int):
        get (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MetricCollectionResponseBody]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        vertexid=vertexid,
        subtaskindex=subtaskindex,
        get=get,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    jobid: str,
    vertexid: str,
    subtaskindex: int,
    *,
    client: Union[AuthenticatedClient, Client],
    get: Union[Unset, str] = UNSET,
) -> Optional[MetricCollectionResponseBody]:
    """Provides access to subtask metrics.

    Args:
        jobid (str):
        vertexid (str):
        subtaskindex (int):
        get (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MetricCollectionResponseBody
    """

    return (
        await asyncio_detailed(
            jobid=jobid,
            vertexid=vertexid,
            subtaskindex=subtaskindex,
            client=client,
            get=get,
        )
    ).parsed
