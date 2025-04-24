from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Parallelism")


@_attrs_define
class Parallelism:
    """
    Attributes:
        lower_bound (Union[Unset, int]):
        upper_bound (Union[Unset, int]):
    """

    lower_bound: Union[Unset, int] = UNSET
    upper_bound: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lower_bound = self.lower_bound

        upper_bound = self.upper_bound

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if lower_bound is not UNSET:
            field_dict["lowerBound"] = lower_bound
        if upper_bound is not UNSET:
            field_dict["upperBound"] = upper_bound

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        lower_bound = d.pop("lowerBound", UNSET)

        upper_bound = d.pop("upperBound", UNSET)

        parallelism = cls(
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )

        parallelism.additional_properties = d
        return parallelism

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
