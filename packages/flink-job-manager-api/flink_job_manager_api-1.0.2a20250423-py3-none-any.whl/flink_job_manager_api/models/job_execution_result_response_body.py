from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_result import JobResult
    from ..models.queue_status import QueueStatus


T = TypeVar("T", bound="JobExecutionResultResponseBody")


@_attrs_define
class JobExecutionResultResponseBody:
    """
    Attributes:
        status (QueueStatus):
        job_execution_result (Union[Unset, JobResult]):
    """

    status: "QueueStatus"
    job_execution_result: Union[Unset, "JobResult"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.to_dict()

        job_execution_result: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.job_execution_result, Unset):
            job_execution_result = self.job_execution_result.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )
        if job_execution_result is not UNSET:
            field_dict["job-execution-result"] = job_execution_result

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.job_result import JobResult
        from ..models.queue_status import QueueStatus

        d = src_dict.copy()
        status = QueueStatus.from_dict(d.pop("status"))

        _job_execution_result = d.pop("job-execution-result", UNSET)
        job_execution_result: Union[Unset, JobResult]
        if isinstance(_job_execution_result, Unset):
            job_execution_result = UNSET
        else:
            job_execution_result = JobResult.from_dict(_job_execution_result)

        job_execution_result_response_body = cls(
            status=status,
            job_execution_result=job_execution_result,
        )

        job_execution_result_response_body.additional_properties = d
        return job_execution_result_response_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
