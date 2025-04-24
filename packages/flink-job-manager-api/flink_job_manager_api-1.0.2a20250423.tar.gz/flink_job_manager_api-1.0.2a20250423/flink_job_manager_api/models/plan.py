from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plan_node import PlanNode


T = TypeVar("T", bound="Plan")


@_attrs_define
class Plan:
    """
    Attributes:
        jid (Union[Unset, str]):
        name (Union[Unset, str]):
        nodes (Union[Unset, list['PlanNode']]):
        type_ (Union[Unset, str]):
    """

    jid: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    nodes: Union[Unset, list["PlanNode"]] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        jid = self.jid

        name = self.name

        nodes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.nodes, Unset):
            nodes = []
            for nodes_item_data in self.nodes:
                nodes_item = nodes_item_data.to_dict()
                nodes.append(nodes_item)

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if jid is not UNSET:
            field_dict["jid"] = jid
        if name is not UNSET:
            field_dict["name"] = name
        if nodes is not UNSET:
            field_dict["nodes"] = nodes
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.plan_node import PlanNode

        d = src_dict.copy()
        jid = d.pop("jid", UNSET)

        name = d.pop("name", UNSET)

        nodes = []
        _nodes = d.pop("nodes", UNSET)
        for nodes_item_data in _nodes or []:
            nodes_item = PlanNode.from_dict(nodes_item_data)

            nodes.append(nodes_item)

        type_ = d.pop("type", UNSET)

        plan = cls(
            jid=jid,
            name=name,
            nodes=nodes,
            type_=type_,
        )

        plan.additional_properties = d
        return plan

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
