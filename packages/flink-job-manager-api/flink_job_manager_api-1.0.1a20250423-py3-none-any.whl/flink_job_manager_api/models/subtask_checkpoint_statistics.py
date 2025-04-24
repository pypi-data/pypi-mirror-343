from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubtaskCheckpointStatistics")


@_attrs_define
class SubtaskCheckpointStatistics:
    """
    Attributes:
        class_name (str):
        index (Union[Unset, int]):
        status (Union[Unset, str]):
    """

    class_name: str
    index: Union[Unset, int] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        class_name = self.class_name

        index = self.index

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "className": class_name,
            }
        )
        if index is not UNSET:
            field_dict["index"] = index
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        class_name = d.pop("className")

        index = d.pop("index", UNSET)

        status = d.pop("status", UNSET)

        subtask_checkpoint_statistics = cls(
            class_name=class_name,
            index=index,
            status=status,
        )

        subtask_checkpoint_statistics.additional_properties = d
        return subtask_checkpoint_statistics

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
