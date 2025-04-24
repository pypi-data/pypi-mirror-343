from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExternalizedCheckpointInfo")


@_attrs_define
class ExternalizedCheckpointInfo:
    """
    Attributes:
        delete_on_cancellation (Union[Unset, bool]):
        enabled (Union[Unset, bool]):
    """

    delete_on_cancellation: Union[Unset, bool] = UNSET
    enabled: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        delete_on_cancellation = self.delete_on_cancellation

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if delete_on_cancellation is not UNSET:
            field_dict["delete_on_cancellation"] = delete_on_cancellation
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        delete_on_cancellation = d.pop("delete_on_cancellation", UNSET)

        enabled = d.pop("enabled", UNSET)

        externalized_checkpoint_info = cls(
            delete_on_cancellation=delete_on_cancellation,
            enabled=enabled,
        )

        externalized_checkpoint_info.additional_properties = d
        return externalized_checkpoint_info

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
