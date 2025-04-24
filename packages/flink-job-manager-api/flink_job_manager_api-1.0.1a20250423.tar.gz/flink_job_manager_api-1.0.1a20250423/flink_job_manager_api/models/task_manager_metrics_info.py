from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.garbage_collector_info import GarbageCollectorInfo


T = TypeVar("T", bound="TaskManagerMetricsInfo")


@_attrs_define
class TaskManagerMetricsInfo:
    """
    Attributes:
        direct_count (Union[Unset, int]):
        direct_max (Union[Unset, int]):
        direct_used (Union[Unset, int]):
        garbage_collectors (Union[Unset, list['GarbageCollectorInfo']]):
        heap_committed (Union[Unset, int]):
        heap_max (Union[Unset, int]):
        heap_used (Union[Unset, int]):
        mapped_count (Union[Unset, int]):
        mapped_max (Union[Unset, int]):
        mapped_used (Union[Unset, int]):
        netty_shuffle_memory_available (Union[Unset, int]):
        netty_shuffle_memory_segments_available (Union[Unset, int]):
        netty_shuffle_memory_segments_total (Union[Unset, int]):
        netty_shuffle_memory_segments_used (Union[Unset, int]):
        netty_shuffle_memory_total (Union[Unset, int]):
        netty_shuffle_memory_used (Union[Unset, int]):
        non_heap_committed (Union[Unset, int]):
        non_heap_max (Union[Unset, int]):
        non_heap_used (Union[Unset, int]):
    """

    direct_count: Union[Unset, int] = UNSET
    direct_max: Union[Unset, int] = UNSET
    direct_used: Union[Unset, int] = UNSET
    garbage_collectors: Union[Unset, list["GarbageCollectorInfo"]] = UNSET
    heap_committed: Union[Unset, int] = UNSET
    heap_max: Union[Unset, int] = UNSET
    heap_used: Union[Unset, int] = UNSET
    mapped_count: Union[Unset, int] = UNSET
    mapped_max: Union[Unset, int] = UNSET
    mapped_used: Union[Unset, int] = UNSET
    netty_shuffle_memory_available: Union[Unset, int] = UNSET
    netty_shuffle_memory_segments_available: Union[Unset, int] = UNSET
    netty_shuffle_memory_segments_total: Union[Unset, int] = UNSET
    netty_shuffle_memory_segments_used: Union[Unset, int] = UNSET
    netty_shuffle_memory_total: Union[Unset, int] = UNSET
    netty_shuffle_memory_used: Union[Unset, int] = UNSET
    non_heap_committed: Union[Unset, int] = UNSET
    non_heap_max: Union[Unset, int] = UNSET
    non_heap_used: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        direct_count = self.direct_count

        direct_max = self.direct_max

        direct_used = self.direct_used

        garbage_collectors: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.garbage_collectors, Unset):
            garbage_collectors = []
            for garbage_collectors_item_data in self.garbage_collectors:
                garbage_collectors_item = garbage_collectors_item_data.to_dict()
                garbage_collectors.append(garbage_collectors_item)

        heap_committed = self.heap_committed

        heap_max = self.heap_max

        heap_used = self.heap_used

        mapped_count = self.mapped_count

        mapped_max = self.mapped_max

        mapped_used = self.mapped_used

        netty_shuffle_memory_available = self.netty_shuffle_memory_available

        netty_shuffle_memory_segments_available = self.netty_shuffle_memory_segments_available

        netty_shuffle_memory_segments_total = self.netty_shuffle_memory_segments_total

        netty_shuffle_memory_segments_used = self.netty_shuffle_memory_segments_used

        netty_shuffle_memory_total = self.netty_shuffle_memory_total

        netty_shuffle_memory_used = self.netty_shuffle_memory_used

        non_heap_committed = self.non_heap_committed

        non_heap_max = self.non_heap_max

        non_heap_used = self.non_heap_used

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if direct_count is not UNSET:
            field_dict["directCount"] = direct_count
        if direct_max is not UNSET:
            field_dict["directMax"] = direct_max
        if direct_used is not UNSET:
            field_dict["directUsed"] = direct_used
        if garbage_collectors is not UNSET:
            field_dict["garbageCollectors"] = garbage_collectors
        if heap_committed is not UNSET:
            field_dict["heapCommitted"] = heap_committed
        if heap_max is not UNSET:
            field_dict["heapMax"] = heap_max
        if heap_used is not UNSET:
            field_dict["heapUsed"] = heap_used
        if mapped_count is not UNSET:
            field_dict["mappedCount"] = mapped_count
        if mapped_max is not UNSET:
            field_dict["mappedMax"] = mapped_max
        if mapped_used is not UNSET:
            field_dict["mappedUsed"] = mapped_used
        if netty_shuffle_memory_available is not UNSET:
            field_dict["nettyShuffleMemoryAvailable"] = netty_shuffle_memory_available
        if netty_shuffle_memory_segments_available is not UNSET:
            field_dict["nettyShuffleMemorySegmentsAvailable"] = netty_shuffle_memory_segments_available
        if netty_shuffle_memory_segments_total is not UNSET:
            field_dict["nettyShuffleMemorySegmentsTotal"] = netty_shuffle_memory_segments_total
        if netty_shuffle_memory_segments_used is not UNSET:
            field_dict["nettyShuffleMemorySegmentsUsed"] = netty_shuffle_memory_segments_used
        if netty_shuffle_memory_total is not UNSET:
            field_dict["nettyShuffleMemoryTotal"] = netty_shuffle_memory_total
        if netty_shuffle_memory_used is not UNSET:
            field_dict["nettyShuffleMemoryUsed"] = netty_shuffle_memory_used
        if non_heap_committed is not UNSET:
            field_dict["nonHeapCommitted"] = non_heap_committed
        if non_heap_max is not UNSET:
            field_dict["nonHeapMax"] = non_heap_max
        if non_heap_used is not UNSET:
            field_dict["nonHeapUsed"] = non_heap_used

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.garbage_collector_info import GarbageCollectorInfo

        d = src_dict.copy()
        direct_count = d.pop("directCount", UNSET)

        direct_max = d.pop("directMax", UNSET)

        direct_used = d.pop("directUsed", UNSET)

        garbage_collectors = []
        _garbage_collectors = d.pop("garbageCollectors", UNSET)
        for garbage_collectors_item_data in _garbage_collectors or []:
            garbage_collectors_item = GarbageCollectorInfo.from_dict(garbage_collectors_item_data)

            garbage_collectors.append(garbage_collectors_item)

        heap_committed = d.pop("heapCommitted", UNSET)

        heap_max = d.pop("heapMax", UNSET)

        heap_used = d.pop("heapUsed", UNSET)

        mapped_count = d.pop("mappedCount", UNSET)

        mapped_max = d.pop("mappedMax", UNSET)

        mapped_used = d.pop("mappedUsed", UNSET)

        netty_shuffle_memory_available = d.pop("nettyShuffleMemoryAvailable", UNSET)

        netty_shuffle_memory_segments_available = d.pop("nettyShuffleMemorySegmentsAvailable", UNSET)

        netty_shuffle_memory_segments_total = d.pop("nettyShuffleMemorySegmentsTotal", UNSET)

        netty_shuffle_memory_segments_used = d.pop("nettyShuffleMemorySegmentsUsed", UNSET)

        netty_shuffle_memory_total = d.pop("nettyShuffleMemoryTotal", UNSET)

        netty_shuffle_memory_used = d.pop("nettyShuffleMemoryUsed", UNSET)

        non_heap_committed = d.pop("nonHeapCommitted", UNSET)

        non_heap_max = d.pop("nonHeapMax", UNSET)

        non_heap_used = d.pop("nonHeapUsed", UNSET)

        task_manager_metrics_info = cls(
            direct_count=direct_count,
            direct_max=direct_max,
            direct_used=direct_used,
            garbage_collectors=garbage_collectors,
            heap_committed=heap_committed,
            heap_max=heap_max,
            heap_used=heap_used,
            mapped_count=mapped_count,
            mapped_max=mapped_max,
            mapped_used=mapped_used,
            netty_shuffle_memory_available=netty_shuffle_memory_available,
            netty_shuffle_memory_segments_available=netty_shuffle_memory_segments_available,
            netty_shuffle_memory_segments_total=netty_shuffle_memory_segments_total,
            netty_shuffle_memory_segments_used=netty_shuffle_memory_segments_used,
            netty_shuffle_memory_total=netty_shuffle_memory_total,
            netty_shuffle_memory_used=netty_shuffle_memory_used,
            non_heap_committed=non_heap_committed,
            non_heap_max=non_heap_max,
            non_heap_used=non_heap_used,
        )

        task_manager_metrics_info.additional_properties = d
        return task_manager_metrics_info

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
