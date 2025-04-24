from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogInfo")


@_attrs_define
class LogInfo:
    """
    Attributes:
        mtime (Union[Unset, int]):
        name (Union[Unset, str]):
        size (Union[Unset, int]):
    """

    mtime: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mtime = self.mtime

        name = self.name

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mtime is not UNSET:
            field_dict["mtime"] = mtime
        if name is not UNSET:
            field_dict["name"] = name
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        mtime = d.pop("mtime", UNSET)

        name = d.pop("name", UNSET)

        size = d.pop("size", UNSET)

        log_info = cls(
            mtime=mtime,
            name=name,
            size=size,
        )

        log_info.additional_properties = d
        return log_info

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
