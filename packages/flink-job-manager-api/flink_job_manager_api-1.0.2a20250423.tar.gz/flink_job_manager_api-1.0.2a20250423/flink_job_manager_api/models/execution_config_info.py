from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.execution_config_info_user_config import ExecutionConfigInfoUserConfig


T = TypeVar("T", bound="ExecutionConfigInfo")


@_attrs_define
class ExecutionConfigInfo:
    """
    Attributes:
        job_parallelism (Union[Unset, int]):
        object_reuse_mode (Union[Unset, bool]):
        restart_strategy (Union[Unset, str]):
        user_config (Union[Unset, ExecutionConfigInfoUserConfig]):
    """

    job_parallelism: Union[Unset, int] = UNSET
    object_reuse_mode: Union[Unset, bool] = UNSET
    restart_strategy: Union[Unset, str] = UNSET
    user_config: Union[Unset, "ExecutionConfigInfoUserConfig"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_parallelism = self.job_parallelism

        object_reuse_mode = self.object_reuse_mode

        restart_strategy = self.restart_strategy

        user_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_config, Unset):
            user_config = self.user_config.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_parallelism is not UNSET:
            field_dict["job-parallelism"] = job_parallelism
        if object_reuse_mode is not UNSET:
            field_dict["object-reuse-mode"] = object_reuse_mode
        if restart_strategy is not UNSET:
            field_dict["restart-strategy"] = restart_strategy
        if user_config is not UNSET:
            field_dict["user-config"] = user_config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.execution_config_info_user_config import ExecutionConfigInfoUserConfig

        d = src_dict.copy()
        job_parallelism = d.pop("job-parallelism", UNSET)

        object_reuse_mode = d.pop("object-reuse-mode", UNSET)

        restart_strategy = d.pop("restart-strategy", UNSET)

        _user_config = d.pop("user-config", UNSET)
        user_config: Union[Unset, ExecutionConfigInfoUserConfig]
        if isinstance(_user_config, Unset):
            user_config = UNSET
        else:
            user_config = ExecutionConfigInfoUserConfig.from_dict(_user_config)

        execution_config_info = cls(
            job_parallelism=job_parallelism,
            object_reuse_mode=object_reuse_mode,
            restart_strategy=restart_strategy,
            user_config=user_config,
        )

        execution_config_info.additional_properties = d
        return execution_config_info

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
