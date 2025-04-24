from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.node import Node


T = TypeVar("T", bound="VertexFlameGraph")


@_attrs_define
class VertexFlameGraph:
    """
    Attributes:
        data (Union[Unset, Node]):
        end_timestamp (Union[Unset, int]):
    """

    data: Union[Unset, "Node"] = UNSET
    end_timestamp: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        end_timestamp = self.end_timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if end_timestamp is not UNSET:
            field_dict["endTimestamp"] = end_timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.node import Node

        d = src_dict.copy()
        _data = d.pop("data", UNSET)
        data: Union[Unset, Node]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = Node.from_dict(_data)

        end_timestamp = d.pop("endTimestamp", UNSET)

        vertex_flame_graph = cls(
            data=data,
            end_timestamp=end_timestamp,
        )

        vertex_flame_graph.additional_properties = d
        return vertex_flame_graph

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
