from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.job_resource_requirements_body import JobResourceRequirementsBody
from ...types import Response


def _get_kwargs(
    jobid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{jobid}/resource-requirements",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[JobResourceRequirementsBody]:
    if response.status_code == 200:
        response_200 = JobResourceRequirementsBody.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[JobResourceRequirementsBody]:
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
) -> Response[JobResourceRequirementsBody]:
    """Request details on the job's resource requirements.

    Args:
        jobid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobResourceRequirementsBody]
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
) -> Optional[JobResourceRequirementsBody]:
    """Request details on the job's resource requirements.

    Args:
        jobid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobResourceRequirementsBody
    """

    return sync_detailed(
        jobid=jobid,
        client=client,
    ).parsed


async def asyncio_detailed(
    jobid: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[JobResourceRequirementsBody]:
    """Request details on the job's resource requirements.

    Args:
        jobid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobResourceRequirementsBody]
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
) -> Optional[JobResourceRequirementsBody]:
    """Request details on the job's resource requirements.

    Args:
        jobid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobResourceRequirementsBody
    """

    return (
        await asyncio_detailed(
            jobid=jobid,
            client=client,
        )
    ).parsed
