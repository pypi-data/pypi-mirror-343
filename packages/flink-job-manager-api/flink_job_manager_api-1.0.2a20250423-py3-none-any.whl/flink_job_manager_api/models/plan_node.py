from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.input_ import Input


T = TypeVar("T", bound="PlanNode")


@_attrs_define
class PlanNode:
    """
    Attributes:
        description (Union[Unset, str]):
        id (Union[Unset, str]):
        inputs (Union[Unset, list['Input']]):
        operator (Union[Unset, str]):
        operator_strategy (Union[Unset, str]):
        optimizer_properties (Union[Unset, str]):
        parallelism (Union[Unset, int]):
    """

    description: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    inputs: Union[Unset, list["Input"]] = UNSET
    operator: Union[Unset, str] = UNSET
    operator_strategy: Union[Unset, str] = UNSET
    optimizer_properties: Union[Unset, str] = UNSET
    parallelism: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        id = self.id

        inputs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.inputs, Unset):
            inputs = []
            for inputs_item_data in self.inputs:
                inputs_item = inputs_item_data.to_dict()
                inputs.append(inputs_item)

        operator = self.operator

        operator_strategy = self.operator_strategy

        optimizer_properties = self.optimizer_properties

        parallelism = self.parallelism

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if id is not UNSET:
            field_dict["id"] = id
        if inputs is not UNSET:
            field_dict["inputs"] = inputs
        if operator is not UNSET:
            field_dict["operator"] = operator
        if operator_strategy is not UNSET:
            field_dict["operator_strategy"] = operator_strategy
        if optimizer_properties is not UNSET:
            field_dict["optimizer_properties"] = optimizer_properties
        if parallelism is not UNSET:
            field_dict["parallelism"] = parallelism

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.input_ import Input

        d = src_dict.copy()
        description = d.pop("description", UNSET)

        id = d.pop("id", UNSET)

        inputs = []
        _inputs = d.pop("inputs", UNSET)
        for inputs_item_data in _inputs or []:
            inputs_item = Input.from_dict(inputs_item_data)

            inputs.append(inputs_item)

        operator = d.pop("operator", UNSET)

        operator_strategy = d.pop("operator_strategy", UNSET)

        optimizer_properties = d.pop("optimizer_properties", UNSET)

        parallelism = d.pop("parallelism", UNSET)

        plan_node = cls(
            description=description,
            id=id,
            inputs=inputs,
            operator=operator,
            operator_strategy=operator_strategy,
            optimizer_properties=optimizer_properties,
            parallelism=parallelism,
        )

        plan_node.additional_properties = d
        return plan_node

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
