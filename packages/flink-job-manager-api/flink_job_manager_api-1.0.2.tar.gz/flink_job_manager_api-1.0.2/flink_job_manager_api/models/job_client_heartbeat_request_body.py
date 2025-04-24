from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobClientHeartbeatRequestBody")


@_attrs_define
class JobClientHeartbeatRequestBody:
    """
    Attributes:
        expired_timestamp (Union[Unset, int]):
    """

    expired_timestamp: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expired_timestamp = self.expired_timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expired_timestamp is not UNSET:
            field_dict["expiredTimestamp"] = expired_timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        expired_timestamp = d.pop("expiredTimestamp", UNSET)

        job_client_heartbeat_request_body = cls(
            expired_timestamp=expired_timestamp,
        )

        job_client_heartbeat_request_body.additional_properties = d
        return job_client_heartbeat_request_body

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
