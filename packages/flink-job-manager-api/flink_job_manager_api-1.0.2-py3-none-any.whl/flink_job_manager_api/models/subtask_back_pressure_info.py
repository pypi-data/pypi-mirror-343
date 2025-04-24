from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vertex_back_pressure_level import VertexBackPressureLevel
from ..types import UNSET, Unset

T = TypeVar("T", bound="SubtaskBackPressureInfo")


@_attrs_define
class SubtaskBackPressureInfo:
    """
    Attributes:
        attempt_number (Union[Unset, int]):
        backpressure_level (Union[Unset, VertexBackPressureLevel]):
        busy_ratio (Union[Unset, float]):
        idle_ratio (Union[Unset, float]):
        other_concurrent_attempts (Union[Unset, list['SubtaskBackPressureInfo']]):
        ratio (Union[Unset, float]):
        subtask (Union[Unset, int]):
    """

    attempt_number: Union[Unset, int] = UNSET
    backpressure_level: Union[Unset, VertexBackPressureLevel] = UNSET
    busy_ratio: Union[Unset, float] = UNSET
    idle_ratio: Union[Unset, float] = UNSET
    other_concurrent_attempts: Union[Unset, list["SubtaskBackPressureInfo"]] = UNSET
    ratio: Union[Unset, float] = UNSET
    subtask: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempt_number = self.attempt_number

        backpressure_level: Union[Unset, str] = UNSET
        if not isinstance(self.backpressure_level, Unset):
            backpressure_level = self.backpressure_level.value

        busy_ratio = self.busy_ratio

        idle_ratio = self.idle_ratio

        other_concurrent_attempts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.other_concurrent_attempts, Unset):
            other_concurrent_attempts = []
            for other_concurrent_attempts_item_data in self.other_concurrent_attempts:
                other_concurrent_attempts_item = other_concurrent_attempts_item_data.to_dict()
                other_concurrent_attempts.append(other_concurrent_attempts_item)

        ratio = self.ratio

        subtask = self.subtask

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attempt_number is not UNSET:
            field_dict["attempt-number"] = attempt_number
        if backpressure_level is not UNSET:
            field_dict["backpressureLevel"] = backpressure_level
        if busy_ratio is not UNSET:
            field_dict["busyRatio"] = busy_ratio
        if idle_ratio is not UNSET:
            field_dict["idleRatio"] = idle_ratio
        if other_concurrent_attempts is not UNSET:
            field_dict["other-concurrent-attempts"] = other_concurrent_attempts
        if ratio is not UNSET:
            field_dict["ratio"] = ratio
        if subtask is not UNSET:
            field_dict["subtask"] = subtask

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        attempt_number = d.pop("attempt-number", UNSET)

        _backpressure_level = d.pop("backpressureLevel", UNSET)
        backpressure_level: Union[Unset, VertexBackPressureLevel]
        if isinstance(_backpressure_level, Unset):
            backpressure_level = UNSET
        else:
            backpressure_level = VertexBackPressureLevel(_backpressure_level)

        busy_ratio = d.pop("busyRatio", UNSET)

        idle_ratio = d.pop("idleRatio", UNSET)

        other_concurrent_attempts = []
        _other_concurrent_attempts = d.pop("other-concurrent-attempts", UNSET)
        for other_concurrent_attempts_item_data in _other_concurrent_attempts or []:
            other_concurrent_attempts_item = SubtaskBackPressureInfo.from_dict(other_concurrent_attempts_item_data)

            other_concurrent_attempts.append(other_concurrent_attempts_item)

        ratio = d.pop("ratio", UNSET)

        subtask = d.pop("subtask", UNSET)

        subtask_back_pressure_info = cls(
            attempt_number=attempt_number,
            backpressure_level=backpressure_level,
            busy_ratio=busy_ratio,
            idle_ratio=idle_ratio,
            other_concurrent_attempts=other_concurrent_attempts,
            ratio=ratio,
            subtask=subtask,
        )

        subtask_back_pressure_info.additional_properties = d
        return subtask_back_pressure_info

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
