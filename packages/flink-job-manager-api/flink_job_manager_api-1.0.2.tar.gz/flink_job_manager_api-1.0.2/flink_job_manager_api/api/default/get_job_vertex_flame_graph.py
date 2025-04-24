from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.thread_states import ThreadStates
from ...models.vertex_flame_graph import VertexFlameGraph
from ...types import UNSET, Response, Unset


def _get_kwargs(
    jobid: str,
    vertexid: str,
    *,
    type_: Union[Unset, ThreadStates] = UNSET,
    subtaskindex: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_type_: Union[Unset, str] = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    params["subtaskindex"] = subtaskindex

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{jobid}/vertices/{vertexid}/flamegraph",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[VertexFlameGraph]:
    if response.status_code == 200:
        response_200 = VertexFlameGraph.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[VertexFlameGraph]:
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
    type_: Union[Unset, ThreadStates] = UNSET,
    subtaskindex: Union[Unset, int] = UNSET,
) -> Response[VertexFlameGraph]:
    """Returns flame graph information for a vertex, and may initiate flame graph sampling if necessary.

    Args:
        jobid (str):
        vertexid (str):
        type_ (Union[Unset, ThreadStates]):
        subtaskindex (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VertexFlameGraph]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        vertexid=vertexid,
        type_=type_,
        subtaskindex=subtaskindex,
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
    type_: Union[Unset, ThreadStates] = UNSET,
    subtaskindex: Union[Unset, int] = UNSET,
) -> Optional[VertexFlameGraph]:
    """Returns flame graph information for a vertex, and may initiate flame graph sampling if necessary.

    Args:
        jobid (str):
        vertexid (str):
        type_ (Union[Unset, ThreadStates]):
        subtaskindex (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VertexFlameGraph
    """

    return sync_detailed(
        jobid=jobid,
        vertexid=vertexid,
        client=client,
        type_=type_,
        subtaskindex=subtaskindex,
    ).parsed


async def asyncio_detailed(
    jobid: str,
    vertexid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, ThreadStates] = UNSET,
    subtaskindex: Union[Unset, int] = UNSET,
) -> Response[VertexFlameGraph]:
    """Returns flame graph information for a vertex, and may initiate flame graph sampling if necessary.

    Args:
        jobid (str):
        vertexid (str):
        type_ (Union[Unset, ThreadStates]):
        subtaskindex (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VertexFlameGraph]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        vertexid=vertexid,
        type_=type_,
        subtaskindex=subtaskindex,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    jobid: str,
    vertexid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    type_: Union[Unset, ThreadStates] = UNSET,
    subtaskindex: Union[Unset, int] = UNSET,
) -> Optional[VertexFlameGraph]:
    """Returns flame graph information for a vertex, and may initiate flame graph sampling if necessary.

    Args:
        jobid (str):
        vertexid (str):
        type_ (Union[Unset, ThreadStates]):
        subtaskindex (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VertexFlameGraph
    """

    return (
        await asyncio_detailed(
            jobid=jobid,
            vertexid=vertexid,
            client=client,
            type_=type_,
            subtaskindex=subtaskindex,
        )
    ).parsed
