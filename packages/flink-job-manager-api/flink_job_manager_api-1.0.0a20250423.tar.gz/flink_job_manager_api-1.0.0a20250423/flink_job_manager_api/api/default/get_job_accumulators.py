from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.job_accumulators_info import JobAccumulatorsInfo
from ...types import UNSET, Response, Unset


def _get_kwargs(
    jobid: str,
    *,
    include_serialized_value: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["includeSerializedValue"] = include_serialized_value

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{jobid}/accumulators",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[JobAccumulatorsInfo]:
    if response.status_code == 200:
        response_200 = JobAccumulatorsInfo.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[JobAccumulatorsInfo]:
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
    include_serialized_value: Union[Unset, bool] = UNSET,
) -> Response[JobAccumulatorsInfo]:
    """Returns the accumulators for all tasks of a job, aggregated across the respective subtasks.

    Args:
        jobid (str):
        include_serialized_value (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobAccumulatorsInfo]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        include_serialized_value=include_serialized_value,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_serialized_value: Union[Unset, bool] = UNSET,
) -> Optional[JobAccumulatorsInfo]:
    """Returns the accumulators for all tasks of a job, aggregated across the respective subtasks.

    Args:
        jobid (str):
        include_serialized_value (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobAccumulatorsInfo
    """

    return sync_detailed(
        jobid=jobid,
        client=client,
        include_serialized_value=include_serialized_value,
    ).parsed


async def asyncio_detailed(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_serialized_value: Union[Unset, bool] = UNSET,
) -> Response[JobAccumulatorsInfo]:
    """Returns the accumulators for all tasks of a job, aggregated across the respective subtasks.

    Args:
        jobid (str):
        include_serialized_value (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobAccumulatorsInfo]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        include_serialized_value=include_serialized_value,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_serialized_value: Union[Unset, bool] = UNSET,
) -> Optional[JobAccumulatorsInfo]:
    """Returns the accumulators for all tasks of a job, aggregated across the respective subtasks.

    Args:
        jobid (str):
        include_serialized_value (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobAccumulatorsInfo
    """

    return (
        await asyncio_detailed(
            jobid=jobid,
            client=client,
            include_serialized_value=include_serialized_value,
        )
    ).parsed
