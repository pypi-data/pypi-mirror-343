from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.jar_plan_request_body import JarPlanRequestBody
from ...models.job_plan_info import JobPlanInfo
from ...types import UNSET, Response, Unset


def _get_kwargs(
    jarid: str,
    *,
    body: JarPlanRequestBody,
    program_arg: Union[Unset, str] = UNSET,
    entry_class: Union[Unset, str] = UNSET,
    parallelism: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["programArg"] = program_arg

    params["entry-class"] = entry_class

    params["parallelism"] = parallelism

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/jars/{jarid}/plan",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[JobPlanInfo]:
    if response.status_code == 200:
        response_200 = JobPlanInfo.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[JobPlanInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    jarid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: JarPlanRequestBody,
    program_arg: Union[Unset, str] = UNSET,
    entry_class: Union[Unset, str] = UNSET,
    parallelism: Union[Unset, int] = UNSET,
) -> Response[JobPlanInfo]:
    """Returns the dataflow plan of a job contained in a jar previously uploaded via '/jars/upload'.
    Program arguments can be passed both via the JSON request (recommended) or query parameters.

    Args:
        jarid (str):
        program_arg (Union[Unset, str]):
        entry_class (Union[Unset, str]):
        parallelism (Union[Unset, int]):
        body (JarPlanRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobPlanInfo]
    """

    kwargs = _get_kwargs(
        jarid=jarid,
        body=body,
        program_arg=program_arg,
        entry_class=entry_class,
        parallelism=parallelism,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    jarid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: JarPlanRequestBody,
    program_arg: Union[Unset, str] = UNSET,
    entry_class: Union[Unset, str] = UNSET,
    parallelism: Union[Unset, int] = UNSET,
) -> Optional[JobPlanInfo]:
    """Returns the dataflow plan of a job contained in a jar previously uploaded via '/jars/upload'.
    Program arguments can be passed both via the JSON request (recommended) or query parameters.

    Args:
        jarid (str):
        program_arg (Union[Unset, str]):
        entry_class (Union[Unset, str]):
        parallelism (Union[Unset, int]):
        body (JarPlanRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobPlanInfo
    """

    return sync_detailed(
        jarid=jarid,
        client=client,
        body=body,
        program_arg=program_arg,
        entry_class=entry_class,
        parallelism=parallelism,
    ).parsed


async def asyncio_detailed(
    jarid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: JarPlanRequestBody,
    program_arg: Union[Unset, str] = UNSET,
    entry_class: Union[Unset, str] = UNSET,
    parallelism: Union[Unset, int] = UNSET,
) -> Response[JobPlanInfo]:
    """Returns the dataflow plan of a job contained in a jar previously uploaded via '/jars/upload'.
    Program arguments can be passed both via the JSON request (recommended) or query parameters.

    Args:
        jarid (str):
        program_arg (Union[Unset, str]):
        entry_class (Union[Unset, str]):
        parallelism (Union[Unset, int]):
        body (JarPlanRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobPlanInfo]
    """

    kwargs = _get_kwargs(
        jarid=jarid,
        body=body,
        program_arg=program_arg,
        entry_class=entry_class,
        parallelism=parallelism,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    jarid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: JarPlanRequestBody,
    program_arg: Union[Unset, str] = UNSET,
    entry_class: Union[Unset, str] = UNSET,
    parallelism: Union[Unset, int] = UNSET,
) -> Optional[JobPlanInfo]:
    """Returns the dataflow plan of a job contained in a jar previously uploaded via '/jars/upload'.
    Program arguments can be passed both via the JSON request (recommended) or query parameters.

    Args:
        jarid (str):
        program_arg (Union[Unset, str]):
        entry_class (Union[Unset, str]):
        parallelism (Union[Unset, int]):
        body (JarPlanRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobPlanInfo
    """

    return (
        await asyncio_detailed(
            jarid=jarid,
            client=client,
            body=body,
            program_arg=program_arg,
            entry_class=entry_class,
            parallelism=parallelism,
        )
    ).parsed
