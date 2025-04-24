from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SavepointDisposalRequest")


@_attrs_define
class SavepointDisposalRequest:
    """
    Attributes:
        savepoint_path (Union[Unset, str]):
    """

    savepoint_path: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        savepoint_path = self.savepoint_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if savepoint_path is not UNSET:
            field_dict["savepoint-path"] = savepoint_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        savepoint_path = d.pop("savepoint-path", UNSET)

        savepoint_disposal_request = cls(
            savepoint_path=savepoint_path,
        )

        savepoint_disposal_request.additional_properties = d
        return savepoint_disposal_request

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
