from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RestoredCheckpointStatistics")


@_attrs_define
class RestoredCheckpointStatistics:
    """
    Attributes:
        external_path (Union[Unset, str]):
        id (Union[Unset, int]):
        is_savepoint (Union[Unset, bool]):
        restore_timestamp (Union[Unset, int]):
    """

    external_path: Union[Unset, str] = UNSET
    id: Union[Unset, int] = UNSET
    is_savepoint: Union[Unset, bool] = UNSET
    restore_timestamp: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        external_path = self.external_path

        id = self.id

        is_savepoint = self.is_savepoint

        restore_timestamp = self.restore_timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if external_path is not UNSET:
            field_dict["external_path"] = external_path
        if id is not UNSET:
            field_dict["id"] = id
        if is_savepoint is not UNSET:
            field_dict["is_savepoint"] = is_savepoint
        if restore_timestamp is not UNSET:
            field_dict["restore_timestamp"] = restore_timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        external_path = d.pop("external_path", UNSET)

        id = d.pop("id", UNSET)

        is_savepoint = d.pop("is_savepoint", UNSET)

        restore_timestamp = d.pop("restore_timestamp", UNSET)

        restored_checkpoint_statistics = cls(
            external_path=external_path,
            id=id,
            is_savepoint=is_savepoint,
            restore_timestamp=restore_timestamp,
        )

        restored_checkpoint_statistics.additional_properties = d
        return restored_checkpoint_statistics

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
