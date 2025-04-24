from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.upload_status import UploadStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="JarUploadResponseBody")


@_attrs_define
class JarUploadResponseBody:
    """
    Attributes:
        filename (Union[Unset, str]):
        status (Union[Unset, UploadStatus]):
    """

    filename: Union[Unset, str] = UNSET
    status: Union[Unset, UploadStatus] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filename = self.filename

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filename is not UNSET:
            field_dict["filename"] = filename
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        filename = d.pop("filename", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, UploadStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = UploadStatus(_status)

        jar_upload_response_body = cls(
            filename=filename,
            status=status,
        )

        jar_upload_response_body.additional_properties = d
        return jar_upload_response_body

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
