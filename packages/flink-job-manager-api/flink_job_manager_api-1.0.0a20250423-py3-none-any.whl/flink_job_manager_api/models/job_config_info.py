from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.execution_config_info import ExecutionConfigInfo


T = TypeVar("T", bound="JobConfigInfo")


@_attrs_define
class JobConfigInfo:
    """
    Attributes:
        execution_config_info (Union[Unset, ExecutionConfigInfo]):
        job_id (Union[Unset, str]):
        job_name (Union[Unset, str]):
    """

    execution_config_info: Union[Unset, "ExecutionConfigInfo"] = UNSET
    job_id: Union[Unset, str] = UNSET
    job_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        execution_config_info: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.execution_config_info, Unset):
            execution_config_info = self.execution_config_info.to_dict()

        job_id = self.job_id

        job_name = self.job_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if execution_config_info is not UNSET:
            field_dict["executionConfigInfo"] = execution_config_info
        if job_id is not UNSET:
            field_dict["jobId"] = job_id
        if job_name is not UNSET:
            field_dict["jobName"] = job_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.execution_config_info import ExecutionConfigInfo

        d = src_dict.copy()
        _execution_config_info = d.pop("executionConfigInfo", UNSET)
        execution_config_info: Union[Unset, ExecutionConfigInfo]
        if isinstance(_execution_config_info, Unset):
            execution_config_info = UNSET
        else:
            execution_config_info = ExecutionConfigInfo.from_dict(_execution_config_info)

        job_id = d.pop("jobId", UNSET)

        job_name = d.pop("jobName", UNSET)

        job_config_info = cls(
            execution_config_info=execution_config_info,
            job_id=job_id,
            job_name=job_name,
        )

        job_config_info.additional_properties = d
        return job_config_info

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
