from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_profile_info import ResourceProfileInfo


T = TypeVar("T", bound="SlotInfo")


@_attrs_define
class SlotInfo:
    """
    Attributes:
        job_id (Union[Unset, str]):
        resource (Union[Unset, ResourceProfileInfo]):
    """

    job_id: Union[Unset, str] = UNSET
    resource: Union[Unset, "ResourceProfileInfo"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        resource: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.resource, Unset):
            resource = self.resource.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_id is not UNSET:
            field_dict["jobId"] = job_id
        if resource is not UNSET:
            field_dict["resource"] = resource

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.resource_profile_info import ResourceProfileInfo

        d = src_dict.copy()
        job_id = d.pop("jobId", UNSET)

        _resource = d.pop("resource", UNSET)
        resource: Union[Unset, ResourceProfileInfo]
        if isinstance(_resource, Unset):
            resource = UNSET
        else:
            resource = ResourceProfileInfo.from_dict(_resource)

        slot_info = cls(
            job_id=job_id,
            resource=resource,
        )

        slot_info.additional_properties = d
        return slot_info

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
