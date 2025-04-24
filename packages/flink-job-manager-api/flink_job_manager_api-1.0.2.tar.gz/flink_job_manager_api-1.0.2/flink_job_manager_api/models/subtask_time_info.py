from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subtask_time_info_timestamps import SubtaskTimeInfoTimestamps


T = TypeVar("T", bound="SubtaskTimeInfo")


@_attrs_define
class SubtaskTimeInfo:
    """
    Attributes:
        duration (Union[Unset, int]):
        endpoint (Union[Unset, str]):
        subtask (Union[Unset, int]):
        timestamps (Union[Unset, SubtaskTimeInfoTimestamps]):
    """

    duration: Union[Unset, int] = UNSET
    endpoint: Union[Unset, str] = UNSET
    subtask: Union[Unset, int] = UNSET
    timestamps: Union[Unset, "SubtaskTimeInfoTimestamps"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration = self.duration

        endpoint = self.endpoint

        subtask = self.subtask

        timestamps: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.timestamps, Unset):
            timestamps = self.timestamps.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if duration is not UNSET:
            field_dict["duration"] = duration
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if subtask is not UNSET:
            field_dict["subtask"] = subtask
        if timestamps is not UNSET:
            field_dict["timestamps"] = timestamps

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.subtask_time_info_timestamps import SubtaskTimeInfoTimestamps

        d = src_dict.copy()
        duration = d.pop("duration", UNSET)

        endpoint = d.pop("endpoint", UNSET)

        subtask = d.pop("subtask", UNSET)

        _timestamps = d.pop("timestamps", UNSET)
        timestamps: Union[Unset, SubtaskTimeInfoTimestamps]
        if isinstance(_timestamps, Unset):
            timestamps = UNSET
        else:
            timestamps = SubtaskTimeInfoTimestamps.from_dict(_timestamps)

        subtask_time_info = cls(
            duration=duration,
            endpoint=endpoint,
            subtask=subtask,
            timestamps=timestamps,
        )

        subtask_time_info.additional_properties = d
        return subtask_time_info

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
