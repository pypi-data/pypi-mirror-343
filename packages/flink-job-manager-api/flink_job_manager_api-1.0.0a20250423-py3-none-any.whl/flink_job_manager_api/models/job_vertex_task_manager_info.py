from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.execution_state import ExecutionState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aggregated_task_details_info import AggregatedTaskDetailsInfo
    from ..models.io_metrics_info import IOMetricsInfo
    from ..models.job_vertex_task_manager_info_status_counts import JobVertexTaskManagerInfoStatusCounts


T = TypeVar("T", bound="JobVertexTaskManagerInfo")


@_attrs_define
class JobVertexTaskManagerInfo:
    """
    Attributes:
        aggregated (Union[Unset, AggregatedTaskDetailsInfo]):
        duration (Union[Unset, int]):
        end_time (Union[Unset, int]):
        endpoint (Union[Unset, str]):
        metrics (Union[Unset, IOMetricsInfo]):
        start_time (Union[Unset, int]):
        status (Union[Unset, ExecutionState]):
        status_counts (Union[Unset, JobVertexTaskManagerInfoStatusCounts]):
        taskmanager_id (Union[Unset, str]):
    """

    aggregated: Union[Unset, "AggregatedTaskDetailsInfo"] = UNSET
    duration: Union[Unset, int] = UNSET
    end_time: Union[Unset, int] = UNSET
    endpoint: Union[Unset, str] = UNSET
    metrics: Union[Unset, "IOMetricsInfo"] = UNSET
    start_time: Union[Unset, int] = UNSET
    status: Union[Unset, ExecutionState] = UNSET
    status_counts: Union[Unset, "JobVertexTaskManagerInfoStatusCounts"] = UNSET
    taskmanager_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        aggregated: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.aggregated, Unset):
            aggregated = self.aggregated.to_dict()

        duration = self.duration

        end_time = self.end_time

        endpoint = self.endpoint

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        start_time = self.start_time

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        status_counts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.status_counts, Unset):
            status_counts = self.status_counts.to_dict()

        taskmanager_id = self.taskmanager_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aggregated is not UNSET:
            field_dict["aggregated"] = aggregated
        if duration is not UNSET:
            field_dict["duration"] = duration
        if end_time is not UNSET:
            field_dict["end-time"] = end_time
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if start_time is not UNSET:
            field_dict["start-time"] = start_time
        if status is not UNSET:
            field_dict["status"] = status
        if status_counts is not UNSET:
            field_dict["status-counts"] = status_counts
        if taskmanager_id is not UNSET:
            field_dict["taskmanager-id"] = taskmanager_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.aggregated_task_details_info import AggregatedTaskDetailsInfo
        from ..models.io_metrics_info import IOMetricsInfo
        from ..models.job_vertex_task_manager_info_status_counts import JobVertexTaskManagerInfoStatusCounts

        d = src_dict.copy()
        _aggregated = d.pop("aggregated", UNSET)
        aggregated: Union[Unset, AggregatedTaskDetailsInfo]
        if isinstance(_aggregated, Unset):
            aggregated = UNSET
        else:
            aggregated = AggregatedTaskDetailsInfo.from_dict(_aggregated)

        duration = d.pop("duration", UNSET)

        end_time = d.pop("end-time", UNSET)

        endpoint = d.pop("endpoint", UNSET)

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, IOMetricsInfo]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = IOMetricsInfo.from_dict(_metrics)

        start_time = d.pop("start-time", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ExecutionState]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ExecutionState(_status)

        _status_counts = d.pop("status-counts", UNSET)
        status_counts: Union[Unset, JobVertexTaskManagerInfoStatusCounts]
        if isinstance(_status_counts, Unset):
            status_counts = UNSET
        else:
            status_counts = JobVertexTaskManagerInfoStatusCounts.from_dict(_status_counts)

        taskmanager_id = d.pop("taskmanager-id", UNSET)

        job_vertex_task_manager_info = cls(
            aggregated=aggregated,
            duration=duration,
            end_time=end_time,
            endpoint=endpoint,
            metrics=metrics,
            start_time=start_time,
            status=status,
            status_counts=status_counts,
            taskmanager_id=taskmanager_id,
        )

        job_vertex_task_manager_info.additional_properties = d
        return job_vertex_task_manager_info

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
