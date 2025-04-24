from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.checkpoint_alignment import CheckpointAlignment
    from ..models.checkpoint_duration import CheckpointDuration


T = TypeVar("T", bound="CompletedSubtaskCheckpointStatistics")


@_attrs_define
class CompletedSubtaskCheckpointStatistics:
    """
    Attributes:
        class_name (str):
        index (Union[Unset, int]):
        status (Union[Unset, str]):
        ack_timestamp (Union[Unset, int]):
        end_to_end_duration (Union[Unset, int]):
        checkpointed_size (Union[Unset, int]):
        state_size (Union[Unset, int]):
        checkpoint (Union[Unset, CheckpointDuration]):
        alignment (Union[Unset, CheckpointAlignment]):
        start_delay (Union[Unset, int]):
        unaligned_checkpoint (Union[Unset, bool]):
        aborted (Union[Unset, bool]):
    """

    class_name: str
    index: Union[Unset, int] = UNSET
    status: Union[Unset, str] = UNSET
    ack_timestamp: Union[Unset, int] = UNSET
    end_to_end_duration: Union[Unset, int] = UNSET
    checkpointed_size: Union[Unset, int] = UNSET
    state_size: Union[Unset, int] = UNSET
    checkpoint: Union[Unset, "CheckpointDuration"] = UNSET
    alignment: Union[Unset, "CheckpointAlignment"] = UNSET
    start_delay: Union[Unset, int] = UNSET
    unaligned_checkpoint: Union[Unset, bool] = UNSET
    aborted: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        class_name = self.class_name

        index = self.index

        status = self.status

        ack_timestamp = self.ack_timestamp

        end_to_end_duration = self.end_to_end_duration

        checkpointed_size = self.checkpointed_size

        state_size = self.state_size

        checkpoint: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.checkpoint, Unset):
            checkpoint = self.checkpoint.to_dict()

        alignment: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.alignment, Unset):
            alignment = self.alignment.to_dict()

        start_delay = self.start_delay

        unaligned_checkpoint = self.unaligned_checkpoint

        aborted = self.aborted

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
        if ack_timestamp is not UNSET:
            field_dict["ack_timestamp"] = ack_timestamp
        if end_to_end_duration is not UNSET:
            field_dict["end_to_end_duration"] = end_to_end_duration
        if checkpointed_size is not UNSET:
            field_dict["checkpointed_size"] = checkpointed_size
        if state_size is not UNSET:
            field_dict["state_size"] = state_size
        if checkpoint is not UNSET:
            field_dict["checkpoint"] = checkpoint
        if alignment is not UNSET:
            field_dict["alignment"] = alignment
        if start_delay is not UNSET:
            field_dict["start_delay"] = start_delay
        if unaligned_checkpoint is not UNSET:
            field_dict["unaligned_checkpoint"] = unaligned_checkpoint
        if aborted is not UNSET:
            field_dict["aborted"] = aborted

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.checkpoint_alignment import CheckpointAlignment
        from ..models.checkpoint_duration import CheckpointDuration

        d = src_dict.copy()
        class_name = d.pop("className")

        index = d.pop("index", UNSET)

        status = d.pop("status", UNSET)

        ack_timestamp = d.pop("ack_timestamp", UNSET)

        end_to_end_duration = d.pop("end_to_end_duration", UNSET)

        checkpointed_size = d.pop("checkpointed_size", UNSET)

        state_size = d.pop("state_size", UNSET)

        _checkpoint = d.pop("checkpoint", UNSET)
        checkpoint: Union[Unset, CheckpointDuration]
        if isinstance(_checkpoint, Unset):
            checkpoint = UNSET
        else:
            checkpoint = CheckpointDuration.from_dict(_checkpoint)

        _alignment = d.pop("alignment", UNSET)
        alignment: Union[Unset, CheckpointAlignment]
        if isinstance(_alignment, Unset):
            alignment = UNSET
        else:
            alignment = CheckpointAlignment.from_dict(_alignment)

        start_delay = d.pop("start_delay", UNSET)

        unaligned_checkpoint = d.pop("unaligned_checkpoint", UNSET)

        aborted = d.pop("aborted", UNSET)

        completed_subtask_checkpoint_statistics = cls(
            class_name=class_name,
            index=index,
            status=status,
            ack_timestamp=ack_timestamp,
            end_to_end_duration=end_to_end_duration,
            checkpointed_size=checkpointed_size,
            state_size=state_size,
            checkpoint=checkpoint,
            alignment=alignment,
            start_delay=start_delay,
            unaligned_checkpoint=unaligned_checkpoint,
            aborted=aborted,
        )

        completed_subtask_checkpoint_statistics.additional_properties = d
        return completed_subtask_checkpoint_statistics

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
