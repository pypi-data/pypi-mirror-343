from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.checkpoint_stats_status import CheckpointStatsStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TaskCheckpointStatistics")


@_attrs_define
class TaskCheckpointStatistics:
    """
    Attributes:
        alignment_buffered (Union[Unset, int]):
        checkpointed_size (Union[Unset, int]):
        end_to_end_duration (Union[Unset, int]):
        id (Union[Unset, int]):
        latest_ack_timestamp (Union[Unset, int]):
        num_acknowledged_subtasks (Union[Unset, int]):
        num_subtasks (Union[Unset, int]):
        persisted_data (Union[Unset, int]):
        processed_data (Union[Unset, int]):
        state_size (Union[Unset, int]):
        status (Union[Unset, CheckpointStatsStatus]):
    """

    alignment_buffered: Union[Unset, int] = UNSET
    checkpointed_size: Union[Unset, int] = UNSET
    end_to_end_duration: Union[Unset, int] = UNSET
    id: Union[Unset, int] = UNSET
    latest_ack_timestamp: Union[Unset, int] = UNSET
    num_acknowledged_subtasks: Union[Unset, int] = UNSET
    num_subtasks: Union[Unset, int] = UNSET
    persisted_data: Union[Unset, int] = UNSET
    processed_data: Union[Unset, int] = UNSET
    state_size: Union[Unset, int] = UNSET
    status: Union[Unset, CheckpointStatsStatus] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alignment_buffered = self.alignment_buffered

        checkpointed_size = self.checkpointed_size

        end_to_end_duration = self.end_to_end_duration

        id = self.id

        latest_ack_timestamp = self.latest_ack_timestamp

        num_acknowledged_subtasks = self.num_acknowledged_subtasks

        num_subtasks = self.num_subtasks

        persisted_data = self.persisted_data

        processed_data = self.processed_data

        state_size = self.state_size

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if alignment_buffered is not UNSET:
            field_dict["alignment_buffered"] = alignment_buffered
        if checkpointed_size is not UNSET:
            field_dict["checkpointed_size"] = checkpointed_size
        if end_to_end_duration is not UNSET:
            field_dict["end_to_end_duration"] = end_to_end_duration
        if id is not UNSET:
            field_dict["id"] = id
        if latest_ack_timestamp is not UNSET:
            field_dict["latest_ack_timestamp"] = latest_ack_timestamp
        if num_acknowledged_subtasks is not UNSET:
            field_dict["num_acknowledged_subtasks"] = num_acknowledged_subtasks
        if num_subtasks is not UNSET:
            field_dict["num_subtasks"] = num_subtasks
        if persisted_data is not UNSET:
            field_dict["persisted_data"] = persisted_data
        if processed_data is not UNSET:
            field_dict["processed_data"] = processed_data
        if state_size is not UNSET:
            field_dict["state_size"] = state_size
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        alignment_buffered = d.pop("alignment_buffered", UNSET)

        checkpointed_size = d.pop("checkpointed_size", UNSET)

        end_to_end_duration = d.pop("end_to_end_duration", UNSET)

        id = d.pop("id", UNSET)

        latest_ack_timestamp = d.pop("latest_ack_timestamp", UNSET)

        num_acknowledged_subtasks = d.pop("num_acknowledged_subtasks", UNSET)

        num_subtasks = d.pop("num_subtasks", UNSET)

        persisted_data = d.pop("persisted_data", UNSET)

        processed_data = d.pop("processed_data", UNSET)

        state_size = d.pop("state_size", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, CheckpointStatsStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = CheckpointStatsStatus(_status)

        task_checkpoint_statistics = cls(
            alignment_buffered=alignment_buffered,
            checkpointed_size=checkpointed_size,
            end_to_end_duration=end_to_end_duration,
            id=id,
            latest_ack_timestamp=latest_ack_timestamp,
            num_acknowledged_subtasks=num_acknowledged_subtasks,
            num_subtasks=num_subtasks,
            persisted_data=persisted_data,
            processed_data=processed_data,
            state_size=state_size,
            status=status,
        )

        task_checkpoint_statistics.additional_properties = d
        return task_checkpoint_statistics

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
