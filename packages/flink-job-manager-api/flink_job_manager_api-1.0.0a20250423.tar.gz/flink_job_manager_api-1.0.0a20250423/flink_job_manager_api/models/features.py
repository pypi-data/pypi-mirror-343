from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Features")


@_attrs_define
class Features:
    """
    Attributes:
        web_cancel (Union[Unset, bool]):
        web_history (Union[Unset, bool]):
        web_rescale (Union[Unset, bool]):
        web_submit (Union[Unset, bool]):
    """

    web_cancel: Union[Unset, bool] = UNSET
    web_history: Union[Unset, bool] = UNSET
    web_rescale: Union[Unset, bool] = UNSET
    web_submit: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        web_cancel = self.web_cancel

        web_history = self.web_history

        web_rescale = self.web_rescale

        web_submit = self.web_submit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if web_cancel is not UNSET:
            field_dict["web-cancel"] = web_cancel
        if web_history is not UNSET:
            field_dict["web-history"] = web_history
        if web_rescale is not UNSET:
            field_dict["web-rescale"] = web_rescale
        if web_submit is not UNSET:
            field_dict["web-submit"] = web_submit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        web_cancel = d.pop("web-cancel", UNSET)

        web_history = d.pop("web-history", UNSET)

        web_rescale = d.pop("web-rescale", UNSET)

        web_submit = d.pop("web-submit", UNSET)

        features = cls(
            web_cancel=web_cancel,
            web_history=web_history,
            web_rescale=web_rescale,
            web_submit=web_submit,
        )

        features.additional_properties = d
        return features

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
