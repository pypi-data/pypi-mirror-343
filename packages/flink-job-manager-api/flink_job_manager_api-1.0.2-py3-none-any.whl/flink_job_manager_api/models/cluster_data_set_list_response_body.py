from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cluster_data_set_entry import ClusterDataSetEntry


T = TypeVar("T", bound="ClusterDataSetListResponseBody")


@_attrs_define
class ClusterDataSetListResponseBody:
    """
    Attributes:
        data_sets (Union[Unset, list['ClusterDataSetEntry']]):
    """

    data_sets: Union[Unset, list["ClusterDataSetEntry"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_sets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.data_sets, Unset):
            data_sets = []
            for data_sets_item_data in self.data_sets:
                data_sets_item = data_sets_item_data.to_dict()
                data_sets.append(data_sets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data_sets is not UNSET:
            field_dict["dataSets"] = data_sets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.cluster_data_set_entry import ClusterDataSetEntry

        d = src_dict.copy()
        data_sets = []
        _data_sets = d.pop("dataSets", UNSET)
        for data_sets_item_data in _data_sets or []:
            data_sets_item = ClusterDataSetEntry.from_dict(data_sets_item_data)

            data_sets.append(data_sets_item)

        cluster_data_set_list_response_body = cls(
            data_sets=data_sets,
        )

        cluster_data_set_list_response_body.additional_properties = d
        return cluster_data_set_list_response_body

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
