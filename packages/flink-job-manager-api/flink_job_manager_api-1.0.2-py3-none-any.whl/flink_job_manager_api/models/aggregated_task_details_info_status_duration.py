from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.aggregated_task_details_info_status_duration_additional_property import (
        AggregatedTaskDetailsInfoStatusDurationAdditionalProperty,
    )


T = TypeVar("T", bound="AggregatedTaskDetailsInfoStatusDuration")


@_attrs_define
class AggregatedTaskDetailsInfoStatusDuration:
    """ """

    additional_properties: dict[str, "AggregatedTaskDetailsInfoStatusDurationAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.aggregated_task_details_info_status_duration_additional_property import (
            AggregatedTaskDetailsInfoStatusDurationAdditionalProperty,
        )

        d = src_dict.copy()
        aggregated_task_details_info_status_duration = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = AggregatedTaskDetailsInfoStatusDurationAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        aggregated_task_details_info_status_duration.additional_properties = additional_properties
        return aggregated_task_details_info_status_duration

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "AggregatedTaskDetailsInfoStatusDurationAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "AggregatedTaskDetailsInfoStatusDurationAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
