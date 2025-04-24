from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.stats_summary_dto import StatsSummaryDto


T = TypeVar("T", bound="CheckpointAlignmentSummary")


@_attrs_define
class CheckpointAlignmentSummary:
    """
    Attributes:
        buffered (Union[Unset, StatsSummaryDto]):
        duration (Union[Unset, StatsSummaryDto]):
        persisted (Union[Unset, StatsSummaryDto]):
        processed (Union[Unset, StatsSummaryDto]):
    """

    buffered: Union[Unset, "StatsSummaryDto"] = UNSET
    duration: Union[Unset, "StatsSummaryDto"] = UNSET
    persisted: Union[Unset, "StatsSummaryDto"] = UNSET
    processed: Union[Unset, "StatsSummaryDto"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        buffered: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.buffered, Unset):
            buffered = self.buffered.to_dict()

        duration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.duration, Unset):
            duration = self.duration.to_dict()

        persisted: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.persisted, Unset):
            persisted = self.persisted.to_dict()

        processed: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.processed, Unset):
            processed = self.processed.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if buffered is not UNSET:
            field_dict["buffered"] = buffered
        if duration is not UNSET:
            field_dict["duration"] = duration
        if persisted is not UNSET:
            field_dict["persisted"] = persisted
        if processed is not UNSET:
            field_dict["processed"] = processed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.stats_summary_dto import StatsSummaryDto

        d = src_dict.copy()
        _buffered = d.pop("buffered", UNSET)
        buffered: Union[Unset, StatsSummaryDto]
        if isinstance(_buffered, Unset):
            buffered = UNSET
        else:
            buffered = StatsSummaryDto.from_dict(_buffered)

        _duration = d.pop("duration", UNSET)
        duration: Union[Unset, StatsSummaryDto]
        if isinstance(_duration, Unset):
            duration = UNSET
        else:
            duration = StatsSummaryDto.from_dict(_duration)

        _persisted = d.pop("persisted", UNSET)
        persisted: Union[Unset, StatsSummaryDto]
        if isinstance(_persisted, Unset):
            persisted = UNSET
        else:
            persisted = StatsSummaryDto.from_dict(_persisted)

        _processed = d.pop("processed", UNSET)
        processed: Union[Unset, StatsSummaryDto]
        if isinstance(_processed, Unset):
            processed = UNSET
        else:
            processed = StatsSummaryDto.from_dict(_processed)

        checkpoint_alignment_summary = cls(
            buffered=buffered,
            duration=duration,
            persisted=persisted,
            processed=processed,
        )

        checkpoint_alignment_summary.additional_properties = d
        return checkpoint_alignment_summary

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
