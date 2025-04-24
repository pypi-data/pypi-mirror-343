from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_accumulator import UserAccumulator


T = TypeVar("T", bound="JobVertexAccumulatorsInfo")


@_attrs_define
class JobVertexAccumulatorsInfo:
    """
    Attributes:
        id (Union[Unset, str]):
        user_accumulators (Union[Unset, list['UserAccumulator']]):
    """

    id: Union[Unset, str] = UNSET
    user_accumulators: Union[Unset, list["UserAccumulator"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        user_accumulators: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.user_accumulators, Unset):
            user_accumulators = []
            for user_accumulators_item_data in self.user_accumulators:
                user_accumulators_item = user_accumulators_item_data.to_dict()
                user_accumulators.append(user_accumulators_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if user_accumulators is not UNSET:
            field_dict["user-accumulators"] = user_accumulators

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.user_accumulator import UserAccumulator

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        user_accumulators = []
        _user_accumulators = d.pop("user-accumulators", UNSET)
        for user_accumulators_item_data in _user_accumulators or []:
            user_accumulators_item = UserAccumulator.from_dict(user_accumulators_item_data)

            user_accumulators.append(user_accumulators_item)

        job_vertex_accumulators_info = cls(
            id=id,
            user_accumulators=user_accumulators,
        )

        job_vertex_accumulators_info.additional_properties = d
        return job_vertex_accumulators_info

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
