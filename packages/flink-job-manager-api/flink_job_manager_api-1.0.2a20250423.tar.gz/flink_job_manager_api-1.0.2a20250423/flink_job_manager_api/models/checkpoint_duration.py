from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CheckpointDuration")


@_attrs_define
class CheckpointDuration:
    """
    Attributes:
        async_ (Union[Unset, int]):
        sync (Union[Unset, int]):
    """

    async_: Union[Unset, int] = UNSET
    sync: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        async_ = self.async_

        sync = self.sync

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if async_ is not UNSET:
            field_dict["async"] = async_
        if sync is not UNSET:
            field_dict["sync"] = sync

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        async_ = d.pop("async", UNSET)

        sync = d.pop("sync", UNSET)

        checkpoint_duration = cls(
            async_=async_,
            sync=sync,
        )

        checkpoint_duration.additional_properties = d
        return checkpoint_duration

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
