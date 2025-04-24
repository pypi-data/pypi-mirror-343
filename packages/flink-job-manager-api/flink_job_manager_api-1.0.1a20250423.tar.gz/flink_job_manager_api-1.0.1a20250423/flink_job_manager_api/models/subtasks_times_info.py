from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subtask_time_info import SubtaskTimeInfo


T = TypeVar("T", bound="SubtasksTimesInfo")


@_attrs_define
class SubtasksTimesInfo:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        now (Union[Unset, int]):
        subtasks (Union[Unset, list['SubtaskTimeInfo']]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    now: Union[Unset, int] = UNSET
    subtasks: Union[Unset, list["SubtaskTimeInfo"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        now = self.now

        subtasks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.subtasks, Unset):
            subtasks = []
            for subtasks_item_data in self.subtasks:
                subtasks_item = subtasks_item_data.to_dict()
                subtasks.append(subtasks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if now is not UNSET:
            field_dict["now"] = now
        if subtasks is not UNSET:
            field_dict["subtasks"] = subtasks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.subtask_time_info import SubtaskTimeInfo

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        now = d.pop("now", UNSET)

        subtasks = []
        _subtasks = d.pop("subtasks", UNSET)
        for subtasks_item_data in _subtasks or []:
            subtasks_item = SubtaskTimeInfo.from_dict(subtasks_item_data)

            subtasks.append(subtasks_item)

        subtasks_times_info = cls(
            id=id,
            name=name,
            now=now,
            subtasks=subtasks,
        )

        subtasks_times_info.additional_properties = d
        return subtasks_times_info

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
