from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vertex_back_pressure_level import VertexBackPressureLevel
from ..models.vertex_back_pressure_status import VertexBackPressureStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subtask_back_pressure_info import SubtaskBackPressureInfo


T = TypeVar("T", bound="JobVertexBackPressureInfo")


@_attrs_define
class JobVertexBackPressureInfo:
    """
    Attributes:
        backpressure_level (Union[Unset, VertexBackPressureLevel]):
        end_timestamp (Union[Unset, int]):
        status (Union[Unset, VertexBackPressureStatus]):
        subtasks (Union[Unset, list['SubtaskBackPressureInfo']]):
    """

    backpressure_level: Union[Unset, VertexBackPressureLevel] = UNSET
    end_timestamp: Union[Unset, int] = UNSET
    status: Union[Unset, VertexBackPressureStatus] = UNSET
    subtasks: Union[Unset, list["SubtaskBackPressureInfo"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        backpressure_level: Union[Unset, str] = UNSET
        if not isinstance(self.backpressure_level, Unset):
            backpressure_level = self.backpressure_level.value

        end_timestamp = self.end_timestamp

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        subtasks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.subtasks, Unset):
            subtasks = []
            for subtasks_item_data in self.subtasks:
                subtasks_item = subtasks_item_data.to_dict()
                subtasks.append(subtasks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if backpressure_level is not UNSET:
            field_dict["backpressureLevel"] = backpressure_level
        if end_timestamp is not UNSET:
            field_dict["end-timestamp"] = end_timestamp
        if status is not UNSET:
            field_dict["status"] = status
        if subtasks is not UNSET:
            field_dict["subtasks"] = subtasks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.subtask_back_pressure_info import SubtaskBackPressureInfo

        d = src_dict.copy()
        _backpressure_level = d.pop("backpressureLevel", UNSET)
        backpressure_level: Union[Unset, VertexBackPressureLevel]
        if isinstance(_backpressure_level, Unset):
            backpressure_level = UNSET
        else:
            backpressure_level = VertexBackPressureLevel(_backpressure_level)

        end_timestamp = d.pop("end-timestamp", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, VertexBackPressureStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = VertexBackPressureStatus(_status)

        subtasks = []
        _subtasks = d.pop("subtasks", UNSET)
        for subtasks_item_data in _subtasks or []:
            subtasks_item = SubtaskBackPressureInfo.from_dict(subtasks_item_data)

            subtasks.append(subtasks_item)

        job_vertex_back_pressure_info = cls(
            backpressure_level=backpressure_level,
            end_timestamp=end_timestamp,
            status=status,
            subtasks=subtasks,
        )

        job_vertex_back_pressure_info.additional_properties = d
        return job_vertex_back_pressure_info

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
