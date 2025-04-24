from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.recovery_claim_mode import RecoveryClaimMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.jar_run_request_body_flink_configuration import JarRunRequestBodyFlinkConfiguration


T = TypeVar("T", bound="JarRunRequestBody")


@_attrs_define
class JarRunRequestBody:
    """
    Attributes:
        allow_non_restored_state (Union[Unset, bool]):
        claim_mode (Union[Unset, RecoveryClaimMode]):
        entry_class (Union[Unset, str]):
        flink_configuration (Union[Unset, JarRunRequestBodyFlinkConfiguration]):
        job_id (Union[Unset, str]):
        parallelism (Union[Unset, int]):
        program_args_list (Union[Unset, list[str]]):
        restore_mode (Union[Unset, RecoveryClaimMode]):
        savepoint_path (Union[Unset, str]):
    """

    allow_non_restored_state: Union[Unset, bool] = UNSET
    claim_mode: Union[Unset, RecoveryClaimMode] = UNSET
    entry_class: Union[Unset, str] = UNSET
    flink_configuration: Union[Unset, "JarRunRequestBodyFlinkConfiguration"] = UNSET
    job_id: Union[Unset, str] = UNSET
    parallelism: Union[Unset, int] = UNSET
    program_args_list: Union[Unset, list[str]] = UNSET
    restore_mode: Union[Unset, RecoveryClaimMode] = UNSET
    savepoint_path: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allow_non_restored_state = self.allow_non_restored_state

        claim_mode: Union[Unset, str] = UNSET
        if not isinstance(self.claim_mode, Unset):
            claim_mode = self.claim_mode.value

        entry_class = self.entry_class

        flink_configuration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.flink_configuration, Unset):
            flink_configuration = self.flink_configuration.to_dict()

        job_id = self.job_id

        parallelism = self.parallelism

        program_args_list: Union[Unset, list[str]] = UNSET
        if not isinstance(self.program_args_list, Unset):
            program_args_list = self.program_args_list

        restore_mode: Union[Unset, str] = UNSET
        if not isinstance(self.restore_mode, Unset):
            restore_mode = self.restore_mode.value

        savepoint_path = self.savepoint_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allow_non_restored_state is not UNSET:
            field_dict["allowNonRestoredState"] = allow_non_restored_state
        if claim_mode is not UNSET:
            field_dict["claimMode"] = claim_mode
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
        if restore_mode is not UNSET:
            field_dict["restoreMode"] = restore_mode
        if savepoint_path is not UNSET:
            field_dict["savepointPath"] = savepoint_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.jar_run_request_body_flink_configuration import JarRunRequestBodyFlinkConfiguration

        d = src_dict.copy()
        allow_non_restored_state = d.pop("allowNonRestoredState", UNSET)

        _claim_mode = d.pop("claimMode", UNSET)
        claim_mode: Union[Unset, RecoveryClaimMode]
        if isinstance(_claim_mode, Unset):
            claim_mode = UNSET
        else:
            claim_mode = RecoveryClaimMode(_claim_mode)

        entry_class = d.pop("entryClass", UNSET)

        _flink_configuration = d.pop("flinkConfiguration", UNSET)
        flink_configuration: Union[Unset, JarRunRequestBodyFlinkConfiguration]
        if isinstance(_flink_configuration, Unset):
            flink_configuration = UNSET
        else:
            flink_configuration = JarRunRequestBodyFlinkConfiguration.from_dict(_flink_configuration)

        job_id = d.pop("jobId", UNSET)

        parallelism = d.pop("parallelism", UNSET)

        program_args_list = cast(list[str], d.pop("programArgsList", UNSET))

        _restore_mode = d.pop("restoreMode", UNSET)
        restore_mode: Union[Unset, RecoveryClaimMode]
        if isinstance(_restore_mode, Unset):
            restore_mode = UNSET
        else:
            restore_mode = RecoveryClaimMode(_restore_mode)

        savepoint_path = d.pop("savepointPath", UNSET)

        jar_run_request_body = cls(
            allow_non_restored_state=allow_non_restored_state,
            claim_mode=claim_mode,
            entry_class=entry_class,
            flink_configuration=flink_configuration,
            job_id=job_id,
            parallelism=parallelism,
            program_args_list=program_args_list,
            restore_mode=restore_mode,
            savepoint_path=savepoint_path,
        )

        jar_run_request_body.additional_properties = d
        return jar_run_request_body

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
