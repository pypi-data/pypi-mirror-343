from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.aggregated_metrics_response_body import AggregatedMetricsResponseBody
from ...models.aggregation_mode import AggregationMode
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    get: Union[Unset, str] = UNSET,
    agg: Union[Unset, AggregationMode] = UNSET,
    jobs: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["get"] = get

    json_agg: Union[Unset, str] = UNSET
    if not isinstance(agg, Unset):
        json_agg = agg.value

    params["agg"] = json_agg

    params["jobs"] = jobs

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/jobs/metrics",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AggregatedMetricsResponseBody]:
    if response.status_code == 200:
        response_200 = AggregatedMetricsResponseBody.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AggregatedMetricsResponseBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    get: Union[Unset, str] = UNSET,
    agg: Union[Unset, AggregationMode] = UNSET,
    jobs: Union[Unset, str] = UNSET,
) -> Response[AggregatedMetricsResponseBody]:
    """Provides access to aggregated job metrics.

    Args:
        get (Union[Unset, str]):
        agg (Union[Unset, AggregationMode]):
        jobs (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AggregatedMetricsResponseBody]
    """

    kwargs = _get_kwargs(
        get=get,
        agg=agg,
        jobs=jobs,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    get: Union[Unset, str] = UNSET,
    agg: Union[Unset, AggregationMode] = UNSET,
    jobs: Union[Unset, str] = UNSET,
) -> Optional[AggregatedMetricsResponseBody]:
    """Provides access to aggregated job metrics.

    Args:
        get (Union[Unset, str]):
        agg (Union[Unset, AggregationMode]):
        jobs (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AggregatedMetricsResponseBody
    """

    return sync_detailed(
        client=client,
        get=get,
        agg=agg,
        jobs=jobs,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    get: Union[Unset, str] = UNSET,
    agg: Union[Unset, AggregationMode] = UNSET,
    jobs: Union[Unset, str] = UNSET,
) -> Response[AggregatedMetricsResponseBody]:
    """Provides access to aggregated job metrics.

    Args:
        get (Union[Unset, str]):
        agg (Union[Unset, AggregationMode]):
        jobs (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AggregatedMetricsResponseBody]
    """

    kwargs = _get_kwargs(
        get=get,
        agg=agg,
        jobs=jobs,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    get: Union[Unset, str] = UNSET,
    agg: Union[Unset, AggregationMode] = UNSET,
    jobs: Union[Unset, str] = UNSET,
) -> Optional[AggregatedMetricsResponseBody]:
    """Provides access to aggregated job metrics.

    Args:
        get (Union[Unset, str]):
        agg (Union[Unset, AggregationMode]):
        jobs (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AggregatedMetricsResponseBody
    """

    return (
        await asyncio_detailed(
            client=client,
            get=get,
            agg=agg,
            jobs=jobs,
        )
    ).parsed
