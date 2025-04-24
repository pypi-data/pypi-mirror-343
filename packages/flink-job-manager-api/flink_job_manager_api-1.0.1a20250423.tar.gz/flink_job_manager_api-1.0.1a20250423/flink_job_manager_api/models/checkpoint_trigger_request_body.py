from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.checkpoint_type import CheckpointType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CheckpointTriggerRequestBody")


@_attrs_define
class CheckpointTriggerRequestBody:
    """
    Attributes:
        checkpoint_type (Union[Unset, CheckpointType]):
        trigger_id (Union[Unset, str]):
    """

    checkpoint_type: Union[Unset, CheckpointType] = UNSET
    trigger_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checkpoint_type: Union[Unset, str] = UNSET
        if not isinstance(self.checkpoint_type, Unset):
            checkpoint_type = self.checkpoint_type.value

        trigger_id = self.trigger_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if checkpoint_type is not UNSET:
            field_dict["checkpointType"] = checkpoint_type
        if trigger_id is not UNSET:
            field_dict["triggerId"] = trigger_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _checkpoint_type = d.pop("checkpointType", UNSET)
        checkpoint_type: Union[Unset, CheckpointType]
        if isinstance(_checkpoint_type, Unset):
            checkpoint_type = UNSET
        else:
            checkpoint_type = CheckpointType(_checkpoint_type)

        trigger_id = d.pop("triggerId", UNSET)

        checkpoint_trigger_request_body = cls(
            checkpoint_type=checkpoint_type,
            trigger_id=trigger_id,
        )

        checkpoint_trigger_request_body.additional_properties = d
        return checkpoint_trigger_request_body

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
