from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.savepoint_trigger_request_body import SavepointTriggerRequestBody
from ...models.trigger_response import TriggerResponse
from ...types import Response


def _get_kwargs(
    jobid: str,
    *,
    body: SavepointTriggerRequestBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/jobs/{jobid}/savepoints",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[TriggerResponse]:
    if response.status_code == 202:
        response_202 = TriggerResponse.from_dict(response.json())

        return response_202
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
    body: SavepointTriggerRequestBody,
) -> Response[TriggerResponse]:
    """Triggers a savepoint, and optionally cancels the job afterwards. This async operation would return a
    'triggerid' for further query identifier.

    Args:
        jobid (str):
        body (SavepointTriggerRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerResponse]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SavepointTriggerRequestBody,
) -> Optional[TriggerResponse]:
    """Triggers a savepoint, and optionally cancels the job afterwards. This async operation would return a
    'triggerid' for further query identifier.

    Args:
        jobid (str):
        body (SavepointTriggerRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerResponse
    """

    return sync_detailed(
        jobid=jobid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SavepointTriggerRequestBody,
) -> Response[TriggerResponse]:
    """Triggers a savepoint, and optionally cancels the job afterwards. This async operation would return a
    'triggerid' for further query identifier.

    Args:
        jobid (str):
        body (SavepointTriggerRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerResponse]
    """

    kwargs = _get_kwargs(
        jobid=jobid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SavepointTriggerRequestBody,
) -> Optional[TriggerResponse]:
    """Triggers a savepoint, and optionally cancels the job afterwards. This async operation would return a
    'triggerid' for further query identifier.

    Args:
        jobid (str):
        body (SavepointTriggerRequestBody):

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
            body=body,
        )
    ).parsed
