from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Input")


@_attrs_define
class Input:
    """
    Attributes:
        caching (Union[Unset, str]):
        exchange (Union[Unset, str]):
        id (Union[Unset, str]):
        local_strategy (Union[Unset, str]):
        num (Union[Unset, int]):
        ship_strategy (Union[Unset, str]):
    """

    caching: Union[Unset, str] = UNSET
    exchange: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    local_strategy: Union[Unset, str] = UNSET
    num: Union[Unset, int] = UNSET
    ship_strategy: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        caching = self.caching

        exchange = self.exchange

        id = self.id

        local_strategy = self.local_strategy

        num = self.num

        ship_strategy = self.ship_strategy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if caching is not UNSET:
            field_dict["caching"] = caching
        if exchange is not UNSET:
            field_dict["exchange"] = exchange
        if id is not UNSET:
            field_dict["id"] = id
        if local_strategy is not UNSET:
            field_dict["local_strategy"] = local_strategy
        if num is not UNSET:
            field_dict["num"] = num
        if ship_strategy is not UNSET:
            field_dict["ship_strategy"] = ship_strategy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        caching = d.pop("caching", UNSET)

        exchange = d.pop("exchange", UNSET)

        id = d.pop("id", UNSET)

        local_strategy = d.pop("local_strategy", UNSET)

        num = d.pop("num", UNSET)

        ship_strategy = d.pop("ship_strategy", UNSET)

        input_ = cls(
            caching=caching,
            exchange=exchange,
            id=id,
            local_strategy=local_strategy,
            num=num,
            ship_strategy=ship_strategy,
        )

        input_.additional_properties = d
        return input_

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
