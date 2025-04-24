from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_accumulator import UserAccumulator


T = TypeVar("T", bound="SubtaskAccumulatorsInfo")


@_attrs_define
class SubtaskAccumulatorsInfo:
    """
    Attributes:
        attempt (Union[Unset, int]):
        endpoint (Union[Unset, str]):
        subtask (Union[Unset, int]):
        user_accumulators (Union[Unset, list['UserAccumulator']]):
    """

    attempt: Union[Unset, int] = UNSET
    endpoint: Union[Unset, str] = UNSET
    subtask: Union[Unset, int] = UNSET
    user_accumulators: Union[Unset, list["UserAccumulator"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempt = self.attempt

        endpoint = self.endpoint

        subtask = self.subtask

        user_accumulators: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.user_accumulators, Unset):
            user_accumulators = []
            for user_accumulators_item_data in self.user_accumulators:
                user_accumulators_item = user_accumulators_item_data.to_dict()
                user_accumulators.append(user_accumulators_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attempt is not UNSET:
            field_dict["attempt"] = attempt
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if subtask is not UNSET:
            field_dict["subtask"] = subtask
        if user_accumulators is not UNSET:
            field_dict["user-accumulators"] = user_accumulators

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.user_accumulator import UserAccumulator

        d = src_dict.copy()
        attempt = d.pop("attempt", UNSET)

        endpoint = d.pop("endpoint", UNSET)

        subtask = d.pop("subtask", UNSET)

        user_accumulators = []
        _user_accumulators = d.pop("user-accumulators", UNSET)
        for user_accumulators_item_data in _user_accumulators or []:
            user_accumulators_item = UserAccumulator.from_dict(user_accumulators_item_data)

            user_accumulators.append(user_accumulators_item)

        subtask_accumulators_info = cls(
            attempt=attempt,
            endpoint=endpoint,
            subtask=subtask,
            user_accumulators=user_accumulators,
        )

        subtask_accumulators_info.additional_properties = d
        return subtask_accumulators_info

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
