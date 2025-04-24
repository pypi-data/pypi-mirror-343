from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Counts")


@_attrs_define
class Counts:
    """
    Attributes:
        completed (Union[Unset, int]):
        failed (Union[Unset, int]):
        in_progress (Union[Unset, int]):
        restored (Union[Unset, int]):
        total (Union[Unset, int]):
    """

    completed: Union[Unset, int] = UNSET
    failed: Union[Unset, int] = UNSET
    in_progress: Union[Unset, int] = UNSET
    restored: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        completed = self.completed

        failed = self.failed

        in_progress = self.in_progress

        restored = self.restored

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if completed is not UNSET:
            field_dict["completed"] = completed
        if failed is not UNSET:
            field_dict["failed"] = failed
        if in_progress is not UNSET:
            field_dict["in_progress"] = in_progress
        if restored is not UNSET:
            field_dict["restored"] = restored
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        completed = d.pop("completed", UNSET)

        failed = d.pop("failed", UNSET)

        in_progress = d.pop("in_progress", UNSET)

        restored = d.pop("restored", UNSET)

        total = d.pop("total", UNSET)

        counts = cls(
            completed=completed,
            failed=failed,
            in_progress=in_progress,
            restored=restored,
            total=total,
        )

        counts.additional_properties = d
        return counts

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
