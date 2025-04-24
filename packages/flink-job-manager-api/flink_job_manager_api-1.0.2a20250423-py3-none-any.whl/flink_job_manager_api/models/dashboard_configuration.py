from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.features import Features


T = TypeVar("T", bound="DashboardConfiguration")


@_attrs_define
class DashboardConfiguration:
    """
    Attributes:
        features (Union[Unset, Features]):
        flink_revision (Union[Unset, str]):
        flink_version (Union[Unset, str]):
        refresh_interval (Union[Unset, int]):
        timezone_name (Union[Unset, str]):
        timezone_offset (Union[Unset, int]):
    """

    features: Union[Unset, "Features"] = UNSET
    flink_revision: Union[Unset, str] = UNSET
    flink_version: Union[Unset, str] = UNSET
    refresh_interval: Union[Unset, int] = UNSET
    timezone_name: Union[Unset, str] = UNSET
    timezone_offset: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        features: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.features, Unset):
            features = self.features.to_dict()

        flink_revision = self.flink_revision

        flink_version = self.flink_version

        refresh_interval = self.refresh_interval

        timezone_name = self.timezone_name

        timezone_offset = self.timezone_offset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if features is not UNSET:
            field_dict["features"] = features
        if flink_revision is not UNSET:
            field_dict["flink-revision"] = flink_revision
        if flink_version is not UNSET:
            field_dict["flink-version"] = flink_version
        if refresh_interval is not UNSET:
            field_dict["refresh-interval"] = refresh_interval
        if timezone_name is not UNSET:
            field_dict["timezone-name"] = timezone_name
        if timezone_offset is not UNSET:
            field_dict["timezone-offset"] = timezone_offset

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.features import Features

        d = src_dict.copy()
        _features = d.pop("features", UNSET)
        features: Union[Unset, Features]
        if isinstance(_features, Unset):
            features = UNSET
        else:
            features = Features.from_dict(_features)

        flink_revision = d.pop("flink-revision", UNSET)

        flink_version = d.pop("flink-version", UNSET)

        refresh_interval = d.pop("refresh-interval", UNSET)

        timezone_name = d.pop("timezone-name", UNSET)

        timezone_offset = d.pop("timezone-offset", UNSET)

        dashboard_configuration = cls(
            features=features,
            flink_revision=flink_revision,
            flink_version=flink_version,
            refresh_interval=refresh_interval,
            timezone_name=timezone_name,
            timezone_offset=timezone_offset,
        )

        dashboard_configuration.additional_properties = d
        return dashboard_configuration

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
