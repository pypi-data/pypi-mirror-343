from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.checkpoint_alignment_summary import CheckpointAlignmentSummary
    from ..models.checkpoint_duration_summary import CheckpointDurationSummary
    from ..models.stats_summary_dto import StatsSummaryDto


T = TypeVar("T", bound="TaskCheckpointStatisticsWithSubtaskDetailsSummary")


@_attrs_define
class TaskCheckpointStatisticsWithSubtaskDetailsSummary:
    """
    Attributes:
        alignment (Union[Unset, CheckpointAlignmentSummary]):
        checkpoint_duration (Union[Unset, CheckpointDurationSummary]):
        checkpointed_size (Union[Unset, StatsSummaryDto]):
        end_to_end_duration (Union[Unset, StatsSummaryDto]):
        start_delay (Union[Unset, StatsSummaryDto]):
        state_size (Union[Unset, StatsSummaryDto]):
    """

    alignment: Union[Unset, "CheckpointAlignmentSummary"] = UNSET
    checkpoint_duration: Union[Unset, "CheckpointDurationSummary"] = UNSET
    checkpointed_size: Union[Unset, "StatsSummaryDto"] = UNSET
    end_to_end_duration: Union[Unset, "StatsSummaryDto"] = UNSET
    start_delay: Union[Unset, "StatsSummaryDto"] = UNSET
    state_size: Union[Unset, "StatsSummaryDto"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alignment: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.alignment, Unset):
            alignment = self.alignment.to_dict()

        checkpoint_duration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.checkpoint_duration, Unset):
            checkpoint_duration = self.checkpoint_duration.to_dict()

        checkpointed_size: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.checkpointed_size, Unset):
            checkpointed_size = self.checkpointed_size.to_dict()

        end_to_end_duration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.end_to_end_duration, Unset):
            end_to_end_duration = self.end_to_end_duration.to_dict()

        start_delay: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.start_delay, Unset):
            start_delay = self.start_delay.to_dict()

        state_size: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.state_size, Unset):
            state_size = self.state_size.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if alignment is not UNSET:
            field_dict["alignment"] = alignment
        if checkpoint_duration is not UNSET:
            field_dict["checkpoint_duration"] = checkpoint_duration
        if checkpointed_size is not UNSET:
            field_dict["checkpointed_size"] = checkpointed_size
        if end_to_end_duration is not UNSET:
            field_dict["end_to_end_duration"] = end_to_end_duration
        if start_delay is not UNSET:
            field_dict["start_delay"] = start_delay
        if state_size is not UNSET:
            field_dict["state_size"] = state_size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.checkpoint_alignment_summary import CheckpointAlignmentSummary
        from ..models.checkpoint_duration_summary import CheckpointDurationSummary
        from ..models.stats_summary_dto import StatsSummaryDto

        d = src_dict.copy()
        _alignment = d.pop("alignment", UNSET)
        alignment: Union[Unset, CheckpointAlignmentSummary]
        if isinstance(_alignment, Unset):
            alignment = UNSET
        else:
            alignment = CheckpointAlignmentSummary.from_dict(_alignment)

        _checkpoint_duration = d.pop("checkpoint_duration", UNSET)
        checkpoint_duration: Union[Unset, CheckpointDurationSummary]
        if isinstance(_checkpoint_duration, Unset):
            checkpoint_duration = UNSET
        else:
            checkpoint_duration = CheckpointDurationSummary.from_dict(_checkpoint_duration)

        _checkpointed_size = d.pop("checkpointed_size", UNSET)
        checkpointed_size: Union[Unset, StatsSummaryDto]
        if isinstance(_checkpointed_size, Unset):
            checkpointed_size = UNSET
        else:
            checkpointed_size = StatsSummaryDto.from_dict(_checkpointed_size)

        _end_to_end_duration = d.pop("end_to_end_duration", UNSET)
        end_to_end_duration: Union[Unset, StatsSummaryDto]
        if isinstance(_end_to_end_duration, Unset):
            end_to_end_duration = UNSET
        else:
            end_to_end_duration = StatsSummaryDto.from_dict(_end_to_end_duration)

        _start_delay = d.pop("start_delay", UNSET)
        start_delay: Union[Unset, StatsSummaryDto]
        if isinstance(_start_delay, Unset):
            start_delay = UNSET
        else:
            start_delay = StatsSummaryDto.from_dict(_start_delay)

        _state_size = d.pop("state_size", UNSET)
        state_size: Union[Unset, StatsSummaryDto]
        if isinstance(_state_size, Unset):
            state_size = UNSET
        else:
            state_size = StatsSummaryDto.from_dict(_state_size)

        task_checkpoint_statistics_with_subtask_details_summary = cls(
            alignment=alignment,
            checkpoint_duration=checkpoint_duration,
            checkpointed_size=checkpointed_size,
            end_to_end_duration=end_to_end_duration,
            start_delay=start_delay,
            state_size=state_size,
        )

        task_checkpoint_statistics_with_subtask_details_summary.additional_properties = d
        return task_checkpoint_statistics_with_subtask_details_summary

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
