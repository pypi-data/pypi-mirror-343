from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.stats_summary_dto import StatsSummaryDto


T = TypeVar("T", bound="CheckpointDurationSummary")


@_attrs_define
class CheckpointDurationSummary:
    """
    Attributes:
        async_ (Union[Unset, StatsSummaryDto]):
        sync (Union[Unset, StatsSummaryDto]):
    """

    async_: Union[Unset, "StatsSummaryDto"] = UNSET
    sync: Union[Unset, "StatsSummaryDto"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        async_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.async_, Unset):
            async_ = self.async_.to_dict()

        sync: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sync, Unset):
            sync = self.sync.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if async_ is not UNSET:
            field_dict["async"] = async_
        if sync is not UNSET:
            field_dict["sync"] = sync

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.stats_summary_dto import StatsSummaryDto

        d = src_dict.copy()
        _async_ = d.pop("async", UNSET)
        async_: Union[Unset, StatsSummaryDto]
        if isinstance(_async_, Unset):
            async_ = UNSET
        else:
            async_ = StatsSummaryDto.from_dict(_async_)

        _sync = d.pop("sync", UNSET)
        sync: Union[Unset, StatsSummaryDto]
        if isinstance(_sync, Unset):
            sync = UNSET
        else:
            sync = StatsSummaryDto.from_dict(_sync)

        checkpoint_duration_summary = cls(
            async_=async_,
            sync=sync,
        )

        checkpoint_duration_summary.additional_properties = d
        return checkpoint_duration_summary

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
