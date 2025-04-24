from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SerializedValueOptionalFailureObject")


@_attrs_define
class SerializedValueOptionalFailureObject:
    """
    Attributes:
        byte_array (Union[Unset, list[str]]):
    """

    byte_array: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        byte_array: Union[Unset, list[str]] = UNSET
        if not isinstance(self.byte_array, Unset):
            byte_array = self.byte_array

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if byte_array is not UNSET:
            field_dict["byteArray"] = byte_array

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        byte_array = cast(list[str], d.pop("byteArray", UNSET))

        serialized_value_optional_failure_object = cls(
            byte_array=byte_array,
        )

        serialized_value_optional_failure_object.additional_properties = d
        return serialized_value_optional_failure_object

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
