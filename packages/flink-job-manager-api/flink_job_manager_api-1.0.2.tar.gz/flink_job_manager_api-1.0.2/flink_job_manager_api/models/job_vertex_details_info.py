from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aggregated_task_details_info import AggregatedTaskDetailsInfo
    from ..models.subtask_execution_attempt_details_info import SubtaskExecutionAttemptDetailsInfo


T = TypeVar("T", bound="JobVertexDetailsInfo")


@_attrs_define
class JobVertexDetailsInfo:
    """
    Attributes:
        aggregated (Union[Unset, AggregatedTaskDetailsInfo]):
        id (Union[Unset, str]):
        max_parallelism (Union[Unset, int]):
        name (Union[Unset, str]):
        now (Union[Unset, int]):
        parallelism (Union[Unset, int]):
        subtasks (Union[Unset, list['SubtaskExecutionAttemptDetailsInfo']]):
    """

    aggregated: Union[Unset, "AggregatedTaskDetailsInfo"] = UNSET
    id: Union[Unset, str] = UNSET
    max_parallelism: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    now: Union[Unset, int] = UNSET
    parallelism: Union[Unset, int] = UNSET
    subtasks: Union[Unset, list["SubtaskExecutionAttemptDetailsInfo"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        aggregated: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.aggregated, Unset):
            aggregated = self.aggregated.to_dict()

        id = self.id

        max_parallelism = self.max_parallelism

        name = self.name

        now = self.now

        parallelism = self.parallelism

        subtasks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.subtasks, Unset):
            subtasks = []
            for subtasks_item_data in self.subtasks:
                subtasks_item = subtasks_item_data.to_dict()
                subtasks.append(subtasks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aggregated is not UNSET:
            field_dict["aggregated"] = aggregated
        if id is not UNSET:
            field_dict["id"] = id
        if max_parallelism is not UNSET:
            field_dict["maxParallelism"] = max_parallelism
        if name is not UNSET:
            field_dict["name"] = name
        if now is not UNSET:
            field_dict["now"] = now
        if parallelism is not UNSET:
            field_dict["parallelism"] = parallelism
        if subtasks is not UNSET:
            field_dict["subtasks"] = subtasks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.aggregated_task_details_info import AggregatedTaskDetailsInfo
        from ..models.subtask_execution_attempt_details_info import SubtaskExecutionAttemptDetailsInfo

        d = src_dict.copy()
        _aggregated = d.pop("aggregated", UNSET)
        aggregated: Union[Unset, AggregatedTaskDetailsInfo]
        if isinstance(_aggregated, Unset):
            aggregated = UNSET
        else:
            aggregated = AggregatedTaskDetailsInfo.from_dict(_aggregated)

        id = d.pop("id", UNSET)

        max_parallelism = d.pop("maxParallelism", UNSET)

        name = d.pop("name", UNSET)

        now = d.pop("now", UNSET)

        parallelism = d.pop("parallelism", UNSET)

        subtasks = []
        _subtasks = d.pop("subtasks", UNSET)
        for subtasks_item_data in _subtasks or []:
            subtasks_item = SubtaskExecutionAttemptDetailsInfo.from_dict(subtasks_item_data)

            subtasks.append(subtasks_item)

        job_vertex_details_info = cls(
            aggregated=aggregated,
            id=id,
            max_parallelism=max_parallelism,
            name=name,
            now=now,
            parallelism=parallelism,
            subtasks=subtasks,
        )

        job_vertex_details_info.additional_properties = d
        return job_vertex_details_info

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
