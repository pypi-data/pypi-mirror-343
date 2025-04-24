from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JVMInfo")


@_attrs_define
class JVMInfo:
    """
    Attributes:
        arch (Union[Unset, str]):
        options (Union[Unset, list[str]]):
        version (Union[Unset, str]):
    """

    arch: Union[Unset, str] = UNSET
    options: Union[Unset, list[str]] = UNSET
    version: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        arch = self.arch

        options: Union[Unset, list[str]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if arch is not UNSET:
            field_dict["arch"] = arch
        if options is not UNSET:
            field_dict["options"] = options
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        arch = d.pop("arch", UNSET)

        options = cast(list[str], d.pop("options", UNSET))

        version = d.pop("version", UNSET)

        jvm_info = cls(
            arch=arch,
            options=options,
            version=version,
        )

        jvm_info.additional_properties = d
        return jvm_info

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
