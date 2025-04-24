from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SlotSharingGroupId")


@_attrs_define
class SlotSharingGroupId:
    """
    Attributes:
        bytes_ (Union[Unset, list[str]]):
        lower_part (Union[Unset, int]):
        upper_part (Union[Unset, int]):
    """

    bytes_: Union[Unset, list[str]] = UNSET
    lower_part: Union[Unset, int] = UNSET
    upper_part: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bytes_: Union[Unset, list[str]] = UNSET
        if not isinstance(self.bytes_, Unset):
            bytes_ = self.bytes_

        lower_part = self.lower_part

        upper_part = self.upper_part

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bytes_ is not UNSET:
            field_dict["bytes"] = bytes_
        if lower_part is not UNSET:
            field_dict["lowerPart"] = lower_part
        if upper_part is not UNSET:
            field_dict["upperPart"] = upper_part

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        bytes_ = cast(list[str], d.pop("bytes", UNSET))

        lower_part = d.pop("lowerPart", UNSET)

        upper_part = d.pop("upperPart", UNSET)

        slot_sharing_group_id = cls(
            bytes_=bytes_,
            lower_part=lower_part,
            upper_part=upper_part,
        )

        slot_sharing_group_id.additional_properties = d
        return slot_sharing_group_id

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
