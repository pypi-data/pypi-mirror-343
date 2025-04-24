from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.stats_summary_dto import StatsSummaryDto


T = TypeVar("T", bound="CheckpointStatisticsSummary")


@_attrs_define
class CheckpointStatisticsSummary:
    """
    Attributes:
        alignment_buffered (Union[Unset, StatsSummaryDto]):
        checkpointed_size (Union[Unset, StatsSummaryDto]):
        end_to_end_duration (Union[Unset, StatsSummaryDto]):
        persisted_data (Union[Unset, StatsSummaryDto]):
        processed_data (Union[Unset, StatsSummaryDto]):
        state_size (Union[Unset, StatsSummaryDto]):
    """

    alignment_buffered: Union[Unset, "StatsSummaryDto"] = UNSET
    checkpointed_size: Union[Unset, "StatsSummaryDto"] = UNSET
    end_to_end_duration: Union[Unset, "StatsSummaryDto"] = UNSET
    persisted_data: Union[Unset, "StatsSummaryDto"] = UNSET
    processed_data: Union[Unset, "StatsSummaryDto"] = UNSET
    state_size: Union[Unset, "StatsSummaryDto"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        alignment_buffered: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.alignment_buffered, Unset):
            alignment_buffered = self.alignment_buffered.to_dict()

        checkpointed_size: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.checkpointed_size, Unset):
            checkpointed_size = self.checkpointed_size.to_dict()

        end_to_end_duration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.end_to_end_duration, Unset):
            end_to_end_duration = self.end_to_end_duration.to_dict()

        persisted_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.persisted_data, Unset):
            persisted_data = self.persisted_data.to_dict()

        processed_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.processed_data, Unset):
            processed_data = self.processed_data.to_dict()

        state_size: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.state_size, Unset):
            state_size = self.state_size.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if alignment_buffered is not UNSET:
            field_dict["alignment_buffered"] = alignment_buffered
        if checkpointed_size is not UNSET:
            field_dict["checkpointed_size"] = checkpointed_size
        if end_to_end_duration is not UNSET:
            field_dict["end_to_end_duration"] = end_to_end_duration
        if persisted_data is not UNSET:
            field_dict["persisted_data"] = persisted_data
        if processed_data is not UNSET:
            field_dict["processed_data"] = processed_data
        if state_size is not UNSET:
            field_dict["state_size"] = state_size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.stats_summary_dto import StatsSummaryDto

        d = src_dict.copy()
        _alignment_buffered = d.pop("alignment_buffered", UNSET)
        alignment_buffered: Union[Unset, StatsSummaryDto]
        if isinstance(_alignment_buffered, Unset):
            alignment_buffered = UNSET
        else:
            alignment_buffered = StatsSummaryDto.from_dict(_alignment_buffered)

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

        _persisted_data = d.pop("persisted_data", UNSET)
        persisted_data: Union[Unset, StatsSummaryDto]
        if isinstance(_persisted_data, Unset):
            persisted_data = UNSET
        else:
            persisted_data = StatsSummaryDto.from_dict(_persisted_data)

        _processed_data = d.pop("processed_data", UNSET)
        processed_data: Union[Unset, StatsSummaryDto]
        if isinstance(_processed_data, Unset):
            processed_data = UNSET
        else:
            processed_data = StatsSummaryDto.from_dict(_processed_data)

        _state_size = d.pop("state_size", UNSET)
        state_size: Union[Unset, StatsSummaryDto]
        if isinstance(_state_size, Unset):
            state_size = UNSET
        else:
            state_size = StatsSummaryDto.from_dict(_state_size)

        checkpoint_statistics_summary = cls(
            alignment_buffered=alignment_buffered,
            checkpointed_size=checkpointed_size,
            end_to_end_duration=end_to_end_duration,
            persisted_data=persisted_data,
            processed_data=processed_data,
            state_size=state_size,
        )

        checkpoint_statistics_summary.additional_properties = d
        return checkpoint_statistics_summary

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
