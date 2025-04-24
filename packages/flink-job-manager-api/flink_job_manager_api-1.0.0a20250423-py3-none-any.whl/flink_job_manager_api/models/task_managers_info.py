from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.task_manager_info import TaskManagerInfo


T = TypeVar("T", bound="TaskManagersInfo")


@_attrs_define
class TaskManagersInfo:
    """
    Attributes:
        taskmanagers (Union[Unset, list['TaskManagerInfo']]):
    """

    taskmanagers: Union[Unset, list["TaskManagerInfo"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        taskmanagers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.taskmanagers, Unset):
            taskmanagers = []
            for taskmanagers_item_data in self.taskmanagers:
                taskmanagers_item = taskmanagers_item_data.to_dict()
                taskmanagers.append(taskmanagers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if taskmanagers is not UNSET:
            field_dict["taskmanagers"] = taskmanagers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.task_manager_info import TaskManagerInfo

        d = src_dict.copy()
        taskmanagers = []
        _taskmanagers = d.pop("taskmanagers", UNSET)
        for taskmanagers_item_data in _taskmanagers or []:
            taskmanagers_item = TaskManagerInfo.from_dict(taskmanagers_item_data)

            taskmanagers.append(taskmanagers_item)

        task_managers_info = cls(
            taskmanagers=taskmanagers,
        )

        task_managers_info.additional_properties = d
        return task_managers_info

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
