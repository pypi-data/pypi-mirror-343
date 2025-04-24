from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.failure_label import FailureLabel
from ...models.job_exceptions_info_with_history import JobExceptionsInfoWithHistory
from ...types import UNSET, Response, Unset


def _get_kwargs(
    jobid: str,
    *,
    max_exceptions: Union[Unset, int] = UNSET,
    failure_label_filter: Union[Unset, "FailureLabel"] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["maxExceptions"] = max_exceptions

    json_failure_label_filter: Union[Unset, dict[str, Any]] = UNSET
    if not isinstance(failure_label_filter, Unset):
        json_failure_label_filter = failure_label_filter.to_dict()
    if not isinstance(json_failure_label_filter, Unset):
        params.update(json_failure_label_filter)

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{jobid}/exceptions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[JobExceptionsInfoWithHistory]:
    if response.status_code == 200:
        response_200 = JobExceptionsInfoWithHistory.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[JobExceptionsInfoWithHistory]:
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
    max_exceptions: Union[Unset, int] = UNSET,
    failure_label_filter: Union[Unset, "FailureLabel"] = UNSET,
) -> Response[JobExceptionsInfoWithHistory]:
    """Returns the most recent exceptions that have been handled by Flink for this job. The
    'exceptionHistory.truncated' flag defines whether exceptions were filtered out through the GET
    parameter. The backend collects only a specific amount of most recent exceptions per job. This can
    be configured through web.exception-history-size in the Flink configuration. The following first-
    level members are deprecated: 'root-exception', 'timestamp', 'all-exceptions', and 'truncated'. Use
    the data provided through 'exceptionHistory', instead.

    Args:
        jobid (str):
        max_exceptions (Union[Unset, int]):
        failure_label_filter (Union[Unset, FailureLabel]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobExceptionsInfoWithHistory]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        max_exceptions=max_exceptions,
        failure_label_filter=failure_label_filter,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    max_exceptions: Union[Unset, int] = UNSET,
    failure_label_filter: Union[Unset, "FailureLabel"] = UNSET,
) -> Optional[JobExceptionsInfoWithHistory]:
    """Returns the most recent exceptions that have been handled by Flink for this job. The
    'exceptionHistory.truncated' flag defines whether exceptions were filtered out through the GET
    parameter. The backend collects only a specific amount of most recent exceptions per job. This can
    be configured through web.exception-history-size in the Flink configuration. The following first-
    level members are deprecated: 'root-exception', 'timestamp', 'all-exceptions', and 'truncated'. Use
    the data provided through 'exceptionHistory', instead.

    Args:
        jobid (str):
        max_exceptions (Union[Unset, int]):
        failure_label_filter (Union[Unset, FailureLabel]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobExceptionsInfoWithHistory
    """

    return sync_detailed(
        jobid=jobid,
        client=client,
        max_exceptions=max_exceptions,
        failure_label_filter=failure_label_filter,
    ).parsed


async def asyncio_detailed(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    max_exceptions: Union[Unset, int] = UNSET,
    failure_label_filter: Union[Unset, "FailureLabel"] = UNSET,
) -> Response[JobExceptionsInfoWithHistory]:
    """Returns the most recent exceptions that have been handled by Flink for this job. The
    'exceptionHistory.truncated' flag defines whether exceptions were filtered out through the GET
    parameter. The backend collects only a specific amount of most recent exceptions per job. This can
    be configured through web.exception-history-size in the Flink configuration. The following first-
    level members are deprecated: 'root-exception', 'timestamp', 'all-exceptions', and 'truncated'. Use
    the data provided through 'exceptionHistory', instead.

    Args:
        jobid (str):
        max_exceptions (Union[Unset, int]):
        failure_label_filter (Union[Unset, FailureLabel]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobExceptionsInfoWithHistory]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        max_exceptions=max_exceptions,
        failure_label_filter=failure_label_filter,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    max_exceptions: Union[Unset, int] = UNSET,
    failure_label_filter: Union[Unset, "FailureLabel"] = UNSET,
) -> Optional[JobExceptionsInfoWithHistory]:
    """Returns the most recent exceptions that have been handled by Flink for this job. The
    'exceptionHistory.truncated' flag defines whether exceptions were filtered out through the GET
    parameter. The backend collects only a specific amount of most recent exceptions per job. This can
    be configured through web.exception-history-size in the Flink configuration. The following first-
    level members are deprecated: 'root-exception', 'timestamp', 'all-exceptions', and 'truncated'. Use
    the data provided through 'exceptionHistory', instead.

    Args:
        jobid (str):
        max_exceptions (Union[Unset, int]):
        failure_label_filter (Union[Unset, FailureLabel]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobExceptionsInfoWithHistory
    """

    return (
        await asyncio_detailed(
            jobid=jobid,
            client=client,
            max_exceptions=max_exceptions,
            failure_label_filter=failure_label_filter,
        )
    ).parsed
