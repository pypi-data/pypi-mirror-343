from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.execution_state import ExecutionState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.io_metrics_info import IOMetricsInfo
    from ..models.subtask_execution_attempt_details_info_status_duration import (
        SubtaskExecutionAttemptDetailsInfoStatusDuration,
    )


T = TypeVar("T", bound="SubtaskExecutionAttemptDetailsInfo")


@_attrs_define
class SubtaskExecutionAttemptDetailsInfo:
    """
    Attributes:
        attempt (Union[Unset, int]):
        duration (Union[Unset, int]):
        end_time (Union[Unset, int]):
        endpoint (Union[Unset, str]):
        metrics (Union[Unset, IOMetricsInfo]):
        other_concurrent_attempts (Union[Unset, list['SubtaskExecutionAttemptDetailsInfo']]):
        start_time (Union[Unset, int]):
        status (Union[Unset, ExecutionState]):
        status_duration (Union[Unset, SubtaskExecutionAttemptDetailsInfoStatusDuration]):
        subtask (Union[Unset, int]):
        taskmanager_id (Union[Unset, str]):
    """

    attempt: Union[Unset, int] = UNSET
    duration: Union[Unset, int] = UNSET
    end_time: Union[Unset, int] = UNSET
    endpoint: Union[Unset, str] = UNSET
    metrics: Union[Unset, "IOMetricsInfo"] = UNSET
    other_concurrent_attempts: Union[Unset, list["SubtaskExecutionAttemptDetailsInfo"]] = UNSET
    start_time: Union[Unset, int] = UNSET
    status: Union[Unset, ExecutionState] = UNSET
    status_duration: Union[Unset, "SubtaskExecutionAttemptDetailsInfoStatusDuration"] = UNSET
    subtask: Union[Unset, int] = UNSET
    taskmanager_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempt = self.attempt

        duration = self.duration

        end_time = self.end_time

        endpoint = self.endpoint

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        other_concurrent_attempts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.other_concurrent_attempts, Unset):
            other_concurrent_attempts = []
            for other_concurrent_attempts_item_data in self.other_concurrent_attempts:
                other_concurrent_attempts_item = other_concurrent_attempts_item_data.to_dict()
                other_concurrent_attempts.append(other_concurrent_attempts_item)

        start_time = self.start_time

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        status_duration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.status_duration, Unset):
            status_duration = self.status_duration.to_dict()

        subtask = self.subtask

        taskmanager_id = self.taskmanager_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attempt is not UNSET:
            field_dict["attempt"] = attempt
        if duration is not UNSET:
            field_dict["duration"] = duration
        if end_time is not UNSET:
            field_dict["end-time"] = end_time
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if other_concurrent_attempts is not UNSET:
            field_dict["other-concurrent-attempts"] = other_concurrent_attempts
        if start_time is not UNSET:
            field_dict["start-time"] = start_time
        if status is not UNSET:
            field_dict["status"] = status
        if status_duration is not UNSET:
            field_dict["status-duration"] = status_duration
        if subtask is not UNSET:
            field_dict["subtask"] = subtask
        if taskmanager_id is not UNSET:
            field_dict["taskmanager-id"] = taskmanager_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.io_metrics_info import IOMetricsInfo
        from ..models.subtask_execution_attempt_details_info_status_duration import (
            SubtaskExecutionAttemptDetailsInfoStatusDuration,
        )

        d = src_dict.copy()
        attempt = d.pop("attempt", UNSET)

        duration = d.pop("duration", UNSET)

        end_time = d.pop("end-time", UNSET)

        endpoint = d.pop("endpoint", UNSET)

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, IOMetricsInfo]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = IOMetricsInfo.from_dict(_metrics)

        other_concurrent_attempts = []
        _other_concurrent_attempts = d.pop("other-concurrent-attempts", UNSET)
        for other_concurrent_attempts_item_data in _other_concurrent_attempts or []:
            other_concurrent_attempts_item = SubtaskExecutionAttemptDetailsInfo.from_dict(
                other_concurrent_attempts_item_data
            )

            other_concurrent_attempts.append(other_concurrent_attempts_item)

        start_time = d.pop("start-time", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ExecutionState]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ExecutionState(_status)

        _status_duration = d.pop("status-duration", UNSET)
        status_duration: Union[Unset, SubtaskExecutionAttemptDetailsInfoStatusDuration]
        if isinstance(_status_duration, Unset):
            status_duration = UNSET
        else:
            status_duration = SubtaskExecutionAttemptDetailsInfoStatusDuration.from_dict(_status_duration)

        subtask = d.pop("subtask", UNSET)

        taskmanager_id = d.pop("taskmanager-id", UNSET)

        subtask_execution_attempt_details_info = cls(
            attempt=attempt,
            duration=duration,
            end_time=end_time,
            endpoint=endpoint,
            metrics=metrics,
            other_concurrent_attempts=other_concurrent_attempts,
            start_time=start_time,
            status=status,
            status_duration=status_duration,
            subtask=subtask,
            taskmanager_id=taskmanager_id,
        )

        subtask_execution_attempt_details_info.additional_properties = d
        return subtask_execution_attempt_details_info

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
