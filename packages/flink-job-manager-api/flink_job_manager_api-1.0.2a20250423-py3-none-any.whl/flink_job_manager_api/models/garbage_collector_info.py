from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GarbageCollectorInfo")


@_attrs_define
class GarbageCollectorInfo:
    """
    Attributes:
        count (Union[Unset, int]):
        name (Union[Unset, str]):
        time (Union[Unset, int]):
    """

    count: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    time: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        name = self.name

        time = self.time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if name is not UNSET:
            field_dict["name"] = name
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        count = d.pop("count", UNSET)

        name = d.pop("name", UNSET)

        time = d.pop("time", UNSET)

        garbage_collector_info = cls(
            count=count,
            name=name,
            time=time,
        )

        garbage_collector_info.additional_properties = d
        return garbage_collector_info

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
