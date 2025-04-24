from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HardwareDescription")


@_attrs_define
class HardwareDescription:
    """
    Attributes:
        cpu_cores (Union[Unset, int]):
        free_memory (Union[Unset, int]):
        managed_memory (Union[Unset, int]):
        physical_memory (Union[Unset, int]):
    """

    cpu_cores: Union[Unset, int] = UNSET
    free_memory: Union[Unset, int] = UNSET
    managed_memory: Union[Unset, int] = UNSET
    physical_memory: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cpu_cores = self.cpu_cores

        free_memory = self.free_memory

        managed_memory = self.managed_memory

        physical_memory = self.physical_memory

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cpu_cores is not UNSET:
            field_dict["cpuCores"] = cpu_cores
        if free_memory is not UNSET:
            field_dict["freeMemory"] = free_memory
        if managed_memory is not UNSET:
            field_dict["managedMemory"] = managed_memory
        if physical_memory is not UNSET:
            field_dict["physicalMemory"] = physical_memory

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        cpu_cores = d.pop("cpuCores", UNSET)

        free_memory = d.pop("freeMemory", UNSET)

        managed_memory = d.pop("managedMemory", UNSET)

        physical_memory = d.pop("physicalMemory", UNSET)

        hardware_description = cls(
            cpu_cores=cpu_cores,
            free_memory=free_memory,
            managed_memory=managed_memory,
            physical_memory=physical_memory,
        )

        hardware_description.additional_properties = d
        return hardware_description

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
