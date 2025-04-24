from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StatsSummaryDto")


@_attrs_define
class StatsSummaryDto:
    """
    Attributes:
        avg (Union[Unset, int]):
        max_ (Union[Unset, int]):
        min_ (Union[Unset, int]):
        p50 (Union[Unset, float]):
        p90 (Union[Unset, float]):
        p95 (Union[Unset, float]):
        p99 (Union[Unset, float]):
        p999 (Union[Unset, float]):
    """

    avg: Union[Unset, int] = UNSET
    max_: Union[Unset, int] = UNSET
    min_: Union[Unset, int] = UNSET
    p50: Union[Unset, float] = UNSET
    p90: Union[Unset, float] = UNSET
    p95: Union[Unset, float] = UNSET
    p99: Union[Unset, float] = UNSET
    p999: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avg = self.avg

        max_ = self.max_

        min_ = self.min_

        p50 = self.p50

        p90 = self.p90

        p95 = self.p95

        p99 = self.p99

        p999 = self.p999

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avg is not UNSET:
            field_dict["avg"] = avg
        if max_ is not UNSET:
            field_dict["max"] = max_
        if min_ is not UNSET:
            field_dict["min"] = min_
        if p50 is not UNSET:
            field_dict["p50"] = p50
        if p90 is not UNSET:
            field_dict["p90"] = p90
        if p95 is not UNSET:
            field_dict["p95"] = p95
        if p99 is not UNSET:
            field_dict["p99"] = p99
        if p999 is not UNSET:
            field_dict["p999"] = p999

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        avg = d.pop("avg", UNSET)

        max_ = d.pop("max", UNSET)

        min_ = d.pop("min", UNSET)

        p50 = d.pop("p50", UNSET)

        p90 = d.pop("p90", UNSET)

        p95 = d.pop("p95", UNSET)

        p99 = d.pop("p99", UNSET)

        p999 = d.pop("p999", UNSET)

        stats_summary_dto = cls(
            avg=avg,
            max_=max_,
            min_=min_,
            p50=p50,
            p90=p90,
            p95=p95,
            p99=p99,
            p999=p999,
        )

        stats_summary_dto.additional_properties = d
        return stats_summary_dto

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
