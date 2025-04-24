from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.jar_plan_request_body_flink_configuration import JarPlanRequestBodyFlinkConfiguration


T = TypeVar("T", bound="JarPlanRequestBody")


@_attrs_define
class JarPlanRequestBody:
    """
    Attributes:
        entry_class (Union[Unset, str]):
        flink_configuration (Union[Unset, JarPlanRequestBodyFlinkConfiguration]):
        job_id (Union[Unset, str]):
        parallelism (Union[Unset, int]):
        program_args_list (Union[Unset, list[str]]):
    """

    entry_class: Union[Unset, str] = UNSET
    flink_configuration: Union[Unset, "JarPlanRequestBodyFlinkConfiguration"] = UNSET
    job_id: Union[Unset, str] = UNSET
    parallelism: Union[Unset, int] = UNSET
    program_args_list: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entry_class = self.entry_class

        flink_configuration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.flink_configuration, Unset):
            flink_configuration = self.flink_configuration.to_dict()

        job_id = self.job_id

        parallelism = self.parallelism

        program_args_list: Union[Unset, list[str]] = UNSET
        if not isinstance(self.program_args_list, Unset):
            program_args_list = self.program_args_list

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if entry_class is not UNSET:
            field_dict["entryClass"] = entry_class
        if flink_configuration is not UNSET:
            field_dict["flinkConfiguration"] = flink_configuration
        if job_id is not UNSET:
            field_dict["jobId"] = job_id
        if parallelism is not UNSET:
            field_dict["parallelism"] = parallelism
        if program_args_list is not UNSET:
            field_dict["programArgsList"] = program_args_list

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.jar_plan_request_body_flink_configuration import JarPlanRequestBodyFlinkConfiguration

        d = src_dict.copy()
        entry_class = d.pop("entryClass", UNSET)

        _flink_configuration = d.pop("flinkConfiguration", UNSET)
        flink_configuration: Union[Unset, JarPlanRequestBodyFlinkConfiguration]
        if isinstance(_flink_configuration, Unset):
            flink_configuration = UNSET
        else:
            flink_configuration = JarPlanRequestBodyFlinkConfiguration.from_dict(_flink_configuration)

        job_id = d.pop("jobId", UNSET)

        parallelism = d.pop("parallelism", UNSET)

        program_args_list = cast(list[str], d.pop("programArgsList", UNSET))

        jar_plan_request_body = cls(
            entry_class=entry_class,
            flink_configuration=flink_configuration,
            job_id=job_id,
            parallelism=parallelism,
            program_args_list=program_args_list,
        )

        jar_plan_request_body.additional_properties = d
        return jar_plan_request_body

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
