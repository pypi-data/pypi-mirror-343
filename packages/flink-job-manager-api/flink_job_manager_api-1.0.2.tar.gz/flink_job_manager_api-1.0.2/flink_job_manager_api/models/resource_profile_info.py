from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_profile_info_extended_resources import ResourceProfileInfoExtendedResources


T = TypeVar("T", bound="ResourceProfileInfo")


@_attrs_define
class ResourceProfileInfo:
    """
    Attributes:
        cpu_cores (Union[Unset, float]):
        extended_resources (Union[Unset, ResourceProfileInfoExtendedResources]):
        managed_memory (Union[Unset, int]):
        network_memory (Union[Unset, int]):
        task_heap_memory (Union[Unset, int]):
        task_off_heap_memory (Union[Unset, int]):
    """

    cpu_cores: Union[Unset, float] = UNSET
    extended_resources: Union[Unset, "ResourceProfileInfoExtendedResources"] = UNSET
    managed_memory: Union[Unset, int] = UNSET
    network_memory: Union[Unset, int] = UNSET
    task_heap_memory: Union[Unset, int] = UNSET
    task_off_heap_memory: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu_cores = self.cpu_cores

        extended_resources: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.extended_resources, Unset):
            extended_resources = self.extended_resources.to_dict()

        managed_memory = self.managed_memory

        network_memory = self.network_memory

        task_heap_memory = self.task_heap_memory

        task_off_heap_memory = self.task_off_heap_memory

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cpu_cores is not UNSET:
            field_dict["cpuCores"] = cpu_cores
        if extended_resources is not UNSET:
            field_dict["extendedResources"] = extended_resources
        if managed_memory is not UNSET:
            field_dict["managedMemory"] = managed_memory
        if network_memory is not UNSET:
            field_dict["networkMemory"] = network_memory
        if task_heap_memory is not UNSET:
            field_dict["taskHeapMemory"] = task_heap_memory
        if task_off_heap_memory is not UNSET:
            field_dict["taskOffHeapMemory"] = task_off_heap_memory

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.resource_profile_info_extended_resources import ResourceProfileInfoExtendedResources

        d = src_dict.copy()
        cpu_cores = d.pop("cpuCores", UNSET)

        _extended_resources = d.pop("extendedResources", UNSET)
        extended_resources: Union[Unset, ResourceProfileInfoExtendedResources]
        if isinstance(_extended_resources, Unset):
            extended_resources = UNSET
        else:
            extended_resources = ResourceProfileInfoExtendedResources.from_dict(_extended_resources)

        managed_memory = d.pop("managedMemory", UNSET)

        network_memory = d.pop("networkMemory", UNSET)

        task_heap_memory = d.pop("taskHeapMemory", UNSET)

        task_off_heap_memory = d.pop("taskOffHeapMemory", UNSET)

        resource_profile_info = cls(
            cpu_cores=cpu_cores,
            extended_resources=extended_resources,
            managed_memory=managed_memory,
            network_memory=network_memory,
            task_heap_memory=task_heap_memory,
            task_off_heap_memory=task_off_heap_memory,
        )

        resource_profile_info.additional_properties = d
        return resource_profile_info

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
