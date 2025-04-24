from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hardware_description import HardwareDescription
    from ..models.resource_profile_info import ResourceProfileInfo
    from ..models.task_executor_memory_configuration import TaskExecutorMemoryConfiguration


T = TypeVar("T", bound="TaskManagerInfo")


@_attrs_define
class TaskManagerInfo:
    """
    Attributes:
        blocked (Union[Unset, bool]):
        data_port (Union[Unset, int]):
        free_resource (Union[Unset, ResourceProfileInfo]):
        free_slots (Union[Unset, int]):
        hardware (Union[Unset, HardwareDescription]):
        id (Union[Unset, str]):
        jmx_port (Union[Unset, int]):
        memory_configuration (Union[Unset, TaskExecutorMemoryConfiguration]):
        path (Union[Unset, str]):
        slots_number (Union[Unset, int]):
        time_since_last_heartbeat (Union[Unset, int]):
        total_resource (Union[Unset, ResourceProfileInfo]):
    """

    blocked: Union[Unset, bool] = UNSET
    data_port: Union[Unset, int] = UNSET
    free_resource: Union[Unset, "ResourceProfileInfo"] = UNSET
    free_slots: Union[Unset, int] = UNSET
    hardware: Union[Unset, "HardwareDescription"] = UNSET
    id: Union[Unset, str] = UNSET
    jmx_port: Union[Unset, int] = UNSET
    memory_configuration: Union[Unset, "TaskExecutorMemoryConfiguration"] = UNSET
    path: Union[Unset, str] = UNSET
    slots_number: Union[Unset, int] = UNSET
    time_since_last_heartbeat: Union[Unset, int] = UNSET
    total_resource: Union[Unset, "ResourceProfileInfo"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        blocked = self.blocked

        data_port = self.data_port

        free_resource: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.free_resource, Unset):
            free_resource = self.free_resource.to_dict()

        free_slots = self.free_slots

        hardware: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.hardware, Unset):
            hardware = self.hardware.to_dict()

        id = self.id

        jmx_port = self.jmx_port

        memory_configuration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.memory_configuration, Unset):
            memory_configuration = self.memory_configuration.to_dict()

        path = self.path

        slots_number = self.slots_number

        time_since_last_heartbeat = self.time_since_last_heartbeat

        total_resource: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.total_resource, Unset):
            total_resource = self.total_resource.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if blocked is not UNSET:
            field_dict["blocked"] = blocked
        if data_port is not UNSET:
            field_dict["dataPort"] = data_port
        if free_resource is not UNSET:
            field_dict["freeResource"] = free_resource
        if free_slots is not UNSET:
            field_dict["freeSlots"] = free_slots
        if hardware is not UNSET:
            field_dict["hardware"] = hardware
        if id is not UNSET:
            field_dict["id"] = id
        if jmx_port is not UNSET:
            field_dict["jmxPort"] = jmx_port
        if memory_configuration is not UNSET:
            field_dict["memoryConfiguration"] = memory_configuration
        if path is not UNSET:
            field_dict["path"] = path
        if slots_number is not UNSET:
            field_dict["slotsNumber"] = slots_number
        if time_since_last_heartbeat is not UNSET:
            field_dict["timeSinceLastHeartbeat"] = time_since_last_heartbeat
        if total_resource is not UNSET:
            field_dict["totalResource"] = total_resource

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.hardware_description import HardwareDescription
        from ..models.resource_profile_info import ResourceProfileInfo
        from ..models.task_executor_memory_configuration import TaskExecutorMemoryConfiguration

        d = src_dict.copy()
        blocked = d.pop("blocked", UNSET)

        data_port = d.pop("dataPort", UNSET)

        _free_resource = d.pop("freeResource", UNSET)
        free_resource: Union[Unset, ResourceProfileInfo]
        if isinstance(_free_resource, Unset):
            free_resource = UNSET
        else:
            free_resource = ResourceProfileInfo.from_dict(_free_resource)

        free_slots = d.pop("freeSlots", UNSET)

        _hardware = d.pop("hardware", UNSET)
        hardware: Union[Unset, HardwareDescription]
        if isinstance(_hardware, Unset):
            hardware = UNSET
        else:
            hardware = HardwareDescription.from_dict(_hardware)

        id = d.pop("id", UNSET)

        jmx_port = d.pop("jmxPort", UNSET)

        _memory_configuration = d.pop("memoryConfiguration", UNSET)
        memory_configuration: Union[Unset, TaskExecutorMemoryConfiguration]
        if isinstance(_memory_configuration, Unset):
            memory_configuration = UNSET
        else:
            memory_configuration = TaskExecutorMemoryConfiguration.from_dict(_memory_configuration)

        path = d.pop("path", UNSET)

        slots_number = d.pop("slotsNumber", UNSET)

        time_since_last_heartbeat = d.pop("timeSinceLastHeartbeat", UNSET)

        _total_resource = d.pop("totalResource", UNSET)
        total_resource: Union[Unset, ResourceProfileInfo]
        if isinstance(_total_resource, Unset):
            total_resource = UNSET
        else:
            total_resource = ResourceProfileInfo.from_dict(_total_resource)

        task_manager_info = cls(
            blocked=blocked,
            data_port=data_port,
            free_resource=free_resource,
            free_slots=free_slots,
            hardware=hardware,
            id=id,
            jmx_port=jmx_port,
            memory_configuration=memory_configuration,
            path=path,
            slots_number=slots_number,
            time_since_last_heartbeat=time_since_last_heartbeat,
            total_resource=total_resource,
        )

        task_manager_info.additional_properties = d
        return task_manager_info

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
