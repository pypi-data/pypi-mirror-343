from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.serialized_throwable import SerializedThrowable


T = TypeVar("T", bound="CheckpointInfo")


@_attrs_define
class CheckpointInfo:
    """
    Attributes:
        checkpoint_id (Union[Unset, int]):
        failure_cause (Union[Unset, SerializedThrowable]):
    """

    checkpoint_id: Union[Unset, int] = UNSET
    failure_cause: Union[Unset, "SerializedThrowable"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        checkpoint_id = self.checkpoint_id

        failure_cause: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.failure_cause, Unset):
            failure_cause = self.failure_cause.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if checkpoint_id is not UNSET:
            field_dict["checkpointId"] = checkpoint_id
        if failure_cause is not UNSET:
            field_dict["failureCause"] = failure_cause

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.serialized_throwable import SerializedThrowable

        d = src_dict.copy()
        checkpoint_id = d.pop("checkpointId", UNSET)

        _failure_cause = d.pop("failureCause", UNSET)
        failure_cause: Union[Unset, SerializedThrowable]
        if isinstance(_failure_cause, Unset):
            failure_cause = UNSET
        else:
            failure_cause = SerializedThrowable.from_dict(_failure_cause)

        checkpoint_info = cls(
            checkpoint_id=checkpoint_id,
            failure_cause=failure_cause,
        )

        checkpoint_info.additional_properties = d
        return checkpoint_info

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
