from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric import Metric


T = TypeVar("T", bound="MetricCollectionResponseBody")


@_attrs_define
class MetricCollectionResponseBody:
    """
    Attributes:
        metrics (Union[Unset, list['Metric']]):
    """

    metrics: Union[Unset, list["Metric"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metrics: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = []
            for metrics_item_data in self.metrics:
                metrics_item = metrics_item_data.to_dict()
                metrics.append(metrics_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metrics is not UNSET:
            field_dict["metrics"] = metrics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metric import Metric

        d = src_dict.copy()
        metrics = []
        _metrics = d.pop("metrics", UNSET)
        for metrics_item_data in _metrics or []:
            metrics_item = Metric.from_dict(metrics_item_data)

            metrics.append(metrics_item)

        metric_collection_response_body = cls(
            metrics=metrics,
        )

        metric_collection_response_body.additional_properties = d
        return metric_collection_response_body

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
