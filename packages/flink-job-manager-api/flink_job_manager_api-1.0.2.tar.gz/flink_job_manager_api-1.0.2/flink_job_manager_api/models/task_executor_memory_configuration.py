from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TaskExecutorMemoryConfiguration")


@_attrs_define
class TaskExecutorMemoryConfiguration:
    """
    Attributes:
        framework_heap (Union[Unset, int]):
        framework_off_heap (Union[Unset, int]):
        jvm_metaspace (Union[Unset, int]):
        jvm_overhead (Union[Unset, int]):
        managed_memory (Union[Unset, int]):
        network_memory (Union[Unset, int]):
        task_heap (Union[Unset, int]):
        task_off_heap (Union[Unset, int]):
        total_flink_memory (Union[Unset, int]):
        total_process_memory (Union[Unset, int]):
    """

    framework_heap: Union[Unset, int] = UNSET
    framework_off_heap: Union[Unset, int] = UNSET
    jvm_metaspace: Union[Unset, int] = UNSET
    jvm_overhead: Union[Unset, int] = UNSET
    managed_memory: Union[Unset, int] = UNSET
    network_memory: Union[Unset, int] = UNSET
    task_heap: Union[Unset, int] = UNSET
    task_off_heap: Union[Unset, int] = UNSET
    total_flink_memory: Union[Unset, int] = UNSET
    total_process_memory: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        framework_heap = self.framework_heap

        framework_off_heap = self.framework_off_heap

        jvm_metaspace = self.jvm_metaspace

        jvm_overhead = self.jvm_overhead

        managed_memory = self.managed_memory

        network_memory = self.network_memory

        task_heap = self.task_heap

        task_off_heap = self.task_off_heap

        total_flink_memory = self.total_flink_memory

        total_process_memory = self.total_process_memory

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if framework_heap is not UNSET:
            field_dict["frameworkHeap"] = framework_heap
        if framework_off_heap is not UNSET:
            field_dict["frameworkOffHeap"] = framework_off_heap
        if jvm_metaspace is not UNSET:
            field_dict["jvmMetaspace"] = jvm_metaspace
        if jvm_overhead is not UNSET:
            field_dict["jvmOverhead"] = jvm_overhead
        if managed_memory is not UNSET:
            field_dict["managedMemory"] = managed_memory
        if network_memory is not UNSET:
            field_dict["networkMemory"] = network_memory
        if task_heap is not UNSET:
            field_dict["taskHeap"] = task_heap
        if task_off_heap is not UNSET:
            field_dict["taskOffHeap"] = task_off_heap
        if total_flink_memory is not UNSET:
            field_dict["totalFlinkMemory"] = total_flink_memory
        if total_process_memory is not UNSET:
            field_dict["totalProcessMemory"] = total_process_memory

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        framework_heap = d.pop("frameworkHeap", UNSET)

        framework_off_heap = d.pop("frameworkOffHeap", UNSET)

        jvm_metaspace = d.pop("jvmMetaspace", UNSET)

        jvm_overhead = d.pop("jvmOverhead", UNSET)

        managed_memory = d.pop("managedMemory", UNSET)

        network_memory = d.pop("networkMemory", UNSET)

        task_heap = d.pop("taskHeap", UNSET)

        task_off_heap = d.pop("taskOffHeap", UNSET)

        total_flink_memory = d.pop("totalFlinkMemory", UNSET)

        total_process_memory = d.pop("totalProcessMemory", UNSET)

        task_executor_memory_configuration = cls(
            framework_heap=framework_heap,
            framework_off_heap=framework_off_heap,
            jvm_metaspace=jvm_metaspace,
            jvm_overhead=jvm_overhead,
            managed_memory=managed_memory,
            network_memory=network_memory,
            task_heap=task_heap,
            task_off_heap=task_off_heap,
            total_flink_memory=total_flink_memory,
            total_process_memory=total_process_memory,
        )

        task_executor_memory_configuration.additional_properties = d
        return task_executor_memory_configuration

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
