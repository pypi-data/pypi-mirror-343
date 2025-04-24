from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aggregated_task_details_info_metrics import AggregatedTaskDetailsInfoMetrics
    from ..models.aggregated_task_details_info_status_duration import AggregatedTaskDetailsInfoStatusDuration


T = TypeVar("T", bound="AggregatedTaskDetailsInfo")


@_attrs_define
class AggregatedTaskDetailsInfo:
    """
    Attributes:
        metrics (Union[Unset, AggregatedTaskDetailsInfoMetrics]):
        status_duration (Union[Unset, AggregatedTaskDetailsInfoStatusDuration]):
    """

    metrics: Union[Unset, "AggregatedTaskDetailsInfoMetrics"] = UNSET
    status_duration: Union[Unset, "AggregatedTaskDetailsInfoStatusDuration"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        status_duration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.status_duration, Unset):
            status_duration = self.status_duration.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if status_duration is not UNSET:
            field_dict["status-duration"] = status_duration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.aggregated_task_details_info_metrics import AggregatedTaskDetailsInfoMetrics
        from ..models.aggregated_task_details_info_status_duration import AggregatedTaskDetailsInfoStatusDuration

        d = src_dict.copy()
        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, AggregatedTaskDetailsInfoMetrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = AggregatedTaskDetailsInfoMetrics.from_dict(_metrics)

        _status_duration = d.pop("status-duration", UNSET)
        status_duration: Union[Unset, AggregatedTaskDetailsInfoStatusDuration]
        if isinstance(_status_duration, Unset):
            status_duration = UNSET
        else:
            status_duration = AggregatedTaskDetailsInfoStatusDuration.from_dict(_status_duration)

        aggregated_task_details_info = cls(
            metrics=metrics,
            status_duration=status_duration,
        )

        aggregated_task_details_info.additional_properties = d
        return aggregated_task_details_info

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
