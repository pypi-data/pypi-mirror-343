from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.savepoint_format_type import SavepointFormatType
from ..types import UNSET, Unset

T = TypeVar("T", bound="StopWithSavepointRequestBody")


@_attrs_define
class StopWithSavepointRequestBody:
    """
    Attributes:
        drain (Union[Unset, bool]):
        format_type (Union[Unset, SavepointFormatType]):
        target_directory (Union[Unset, str]):
        trigger_id (Union[Unset, str]):
    """

    drain: Union[Unset, bool] = UNSET
    format_type: Union[Unset, SavepointFormatType] = UNSET
    target_directory: Union[Unset, str] = UNSET
    trigger_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        drain = self.drain

        format_type: Union[Unset, str] = UNSET
        if not isinstance(self.format_type, Unset):
            format_type = self.format_type.value

        target_directory = self.target_directory

        trigger_id = self.trigger_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if drain is not UNSET:
            field_dict["drain"] = drain
        if format_type is not UNSET:
            field_dict["formatType"] = format_type
        if target_directory is not UNSET:
            field_dict["targetDirectory"] = target_directory
        if trigger_id is not UNSET:
            field_dict["triggerId"] = trigger_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        drain = d.pop("drain", UNSET)

        _format_type = d.pop("formatType", UNSET)
        format_type: Union[Unset, SavepointFormatType]
        if isinstance(_format_type, Unset):
            format_type = UNSET
        else:
            format_type = SavepointFormatType(_format_type)

        target_directory = d.pop("targetDirectory", UNSET)

        trigger_id = d.pop("triggerId", UNSET)

        stop_with_savepoint_request_body = cls(
            drain=drain,
            format_type=format_type,
            target_directory=target_directory,
            trigger_id=trigger_id,
        )

        stop_with_savepoint_request_body.additional_properties = d
        return stop_with_savepoint_request_body

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
