from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.application_status import ApplicationStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_result_accumulator_results import JobResultAccumulatorResults
    from ..models.serialized_throwable import SerializedThrowable


T = TypeVar("T", bound="JobResult")


@_attrs_define
class JobResult:
    """
    Attributes:
        accumulator_results (Union[Unset, JobResultAccumulatorResults]):
        application_status (Union[Unset, ApplicationStatus]):
        job_id (Union[Unset, str]):
        net_runtime (Union[Unset, int]):
        serialized_throwable (Union[Unset, SerializedThrowable]):
        success (Union[Unset, bool]):
    """

    accumulator_results: Union[Unset, "JobResultAccumulatorResults"] = UNSET
    application_status: Union[Unset, ApplicationStatus] = UNSET
    job_id: Union[Unset, str] = UNSET
    net_runtime: Union[Unset, int] = UNSET
    serialized_throwable: Union[Unset, "SerializedThrowable"] = UNSET
    success: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accumulator_results: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.accumulator_results, Unset):
            accumulator_results = self.accumulator_results.to_dict()

        application_status: Union[Unset, str] = UNSET
        if not isinstance(self.application_status, Unset):
            application_status = self.application_status.value

        job_id = self.job_id

        net_runtime = self.net_runtime

        serialized_throwable: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.serialized_throwable, Unset):
            serialized_throwable = self.serialized_throwable.to_dict()

        success = self.success

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if accumulator_results is not UNSET:
            field_dict["accumulatorResults"] = accumulator_results
        if application_status is not UNSET:
            field_dict["applicationStatus"] = application_status
        if job_id is not UNSET:
            field_dict["jobId"] = job_id
        if net_runtime is not UNSET:
            field_dict["netRuntime"] = net_runtime
        if serialized_throwable is not UNSET:
            field_dict["serializedThrowable"] = serialized_throwable
        if success is not UNSET:
            field_dict["success"] = success

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.job_result_accumulator_results import JobResultAccumulatorResults
        from ..models.serialized_throwable import SerializedThrowable

        d = src_dict.copy()
        _accumulator_results = d.pop("accumulatorResults", UNSET)
        accumulator_results: Union[Unset, JobResultAccumulatorResults]
        if isinstance(_accumulator_results, Unset):
            accumulator_results = UNSET
        else:
            accumulator_results = JobResultAccumulatorResults.from_dict(_accumulator_results)

        _application_status = d.pop("applicationStatus", UNSET)
        application_status: Union[Unset, ApplicationStatus]
        if isinstance(_application_status, Unset):
            application_status = UNSET
        else:
            application_status = ApplicationStatus(_application_status)

        job_id = d.pop("jobId", UNSET)

        net_runtime = d.pop("netRuntime", UNSET)

        _serialized_throwable = d.pop("serializedThrowable", UNSET)
        serialized_throwable: Union[Unset, SerializedThrowable]
        if isinstance(_serialized_throwable, Unset):
            serialized_throwable = UNSET
        else:
            serialized_throwable = SerializedThrowable.from_dict(_serialized_throwable)

        success = d.pop("success", UNSET)

        job_result = cls(
            accumulator_results=accumulator_results,
            application_status=application_status,
            job_id=job_id,
            net_runtime=net_runtime,
            serialized_throwable=serialized_throwable,
            success=success,
        )

        job_result.additional_properties = d
        return job_result

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
