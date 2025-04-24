from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.execution_state import ExecutionState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.io_metrics_info import IOMetricsInfo
    from ..models.job_details_vertex_info_tasks import JobDetailsVertexInfoTasks
    from ..models.slot_sharing_group_id import SlotSharingGroupId


T = TypeVar("T", bound="JobDetailsVertexInfo")


@_attrs_define
class JobDetailsVertexInfo:
    """
    Attributes:
        duration (Union[Unset, int]):
        end_time (Union[Unset, int]):
        id (Union[Unset, str]):
        max_parallelism (Union[Unset, int]):
        metrics (Union[Unset, IOMetricsInfo]):
        name (Union[Unset, str]):
        parallelism (Union[Unset, int]):
        slot_sharing_group_id (Union[Unset, SlotSharingGroupId]):
        start_time (Union[Unset, int]):
        status (Union[Unset, ExecutionState]):
        tasks (Union[Unset, JobDetailsVertexInfoTasks]):
    """

    duration: Union[Unset, int] = UNSET
    end_time: Union[Unset, int] = UNSET
    id: Union[Unset, str] = UNSET
    max_parallelism: Union[Unset, int] = UNSET
    metrics: Union[Unset, "IOMetricsInfo"] = UNSET
    name: Union[Unset, str] = UNSET
    parallelism: Union[Unset, int] = UNSET
    slot_sharing_group_id: Union[Unset, "SlotSharingGroupId"] = UNSET
    start_time: Union[Unset, int] = UNSET
    status: Union[Unset, ExecutionState] = UNSET
    tasks: Union[Unset, "JobDetailsVertexInfoTasks"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration = self.duration

        end_time = self.end_time

        id = self.id

        max_parallelism = self.max_parallelism

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        name = self.name

        parallelism = self.parallelism

        slot_sharing_group_id: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.slot_sharing_group_id, Unset):
            slot_sharing_group_id = self.slot_sharing_group_id.to_dict()

        start_time = self.start_time

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        tasks: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks, Unset):
            tasks = self.tasks.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if duration is not UNSET:
            field_dict["duration"] = duration
        if end_time is not UNSET:
            field_dict["end-time"] = end_time
        if id is not UNSET:
            field_dict["id"] = id
        if max_parallelism is not UNSET:
            field_dict["maxParallelism"] = max_parallelism
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if name is not UNSET:
            field_dict["name"] = name
        if parallelism is not UNSET:
            field_dict["parallelism"] = parallelism
        if slot_sharing_group_id is not UNSET:
            field_dict["slotSharingGroupId"] = slot_sharing_group_id
        if start_time is not UNSET:
            field_dict["start-time"] = start_time
        if status is not UNSET:
            field_dict["status"] = status
        if tasks is not UNSET:
            field_dict["tasks"] = tasks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.io_metrics_info import IOMetricsInfo
        from ..models.job_details_vertex_info_tasks import JobDetailsVertexInfoTasks
        from ..models.slot_sharing_group_id import SlotSharingGroupId

        d = src_dict.copy()
        duration = d.pop("duration", UNSET)

        end_time = d.pop("end-time", UNSET)

        id = d.pop("id", UNSET)

        max_parallelism = d.pop("maxParallelism", UNSET)

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, IOMetricsInfo]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = IOMetricsInfo.from_dict(_metrics)

        name = d.pop("name", UNSET)

        parallelism = d.pop("parallelism", UNSET)

        _slot_sharing_group_id = d.pop("slotSharingGroupId", UNSET)
        slot_sharing_group_id: Union[Unset, SlotSharingGroupId]
        if isinstance(_slot_sharing_group_id, Unset):
            slot_sharing_group_id = UNSET
        else:
            slot_sharing_group_id = SlotSharingGroupId.from_dict(_slot_sharing_group_id)

        start_time = d.pop("start-time", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ExecutionState]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ExecutionState(_status)

        _tasks = d.pop("tasks", UNSET)
        tasks: Union[Unset, JobDetailsVertexInfoTasks]
        if isinstance(_tasks, Unset):
            tasks = UNSET
        else:
            tasks = JobDetailsVertexInfoTasks.from_dict(_tasks)

        job_details_vertex_info = cls(
            duration=duration,
            end_time=end_time,
            id=id,
            max_parallelism=max_parallelism,
            metrics=metrics,
            name=name,
            parallelism=parallelism,
            slot_sharing_group_id=slot_sharing_group_id,
            start_time=start_time,
            status=status,
            tasks=tasks,
        )

        job_details_vertex_info.additional_properties = d
        return job_details_vertex_info

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
