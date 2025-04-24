from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IOMetricsInfo")


@_attrs_define
class IOMetricsInfo:
    """
    Attributes:
        accumulated_backpressured_time (Union[Unset, int]):
        accumulated_busy_time (Union[Unset, float]):
        accumulated_idle_time (Union[Unset, int]):
        read_bytes (Union[Unset, int]):
        read_bytes_complete (Union[Unset, bool]):
        read_records (Union[Unset, int]):
        read_records_complete (Union[Unset, bool]):
        write_bytes (Union[Unset, int]):
        write_bytes_complete (Union[Unset, bool]):
        write_records (Union[Unset, int]):
        write_records_complete (Union[Unset, bool]):
    """

    accumulated_backpressured_time: Union[Unset, int] = UNSET
    accumulated_busy_time: Union[Unset, float] = UNSET
    accumulated_idle_time: Union[Unset, int] = UNSET
    read_bytes: Union[Unset, int] = UNSET
    read_bytes_complete: Union[Unset, bool] = UNSET
    read_records: Union[Unset, int] = UNSET
    read_records_complete: Union[Unset, bool] = UNSET
    write_bytes: Union[Unset, int] = UNSET
    write_bytes_complete: Union[Unset, bool] = UNSET
    write_records: Union[Unset, int] = UNSET
    write_records_complete: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accumulated_backpressured_time = self.accumulated_backpressured_time

        accumulated_busy_time = self.accumulated_busy_time

        accumulated_idle_time = self.accumulated_idle_time

        read_bytes = self.read_bytes

        read_bytes_complete = self.read_bytes_complete

        read_records = self.read_records

        read_records_complete = self.read_records_complete

        write_bytes = self.write_bytes

        write_bytes_complete = self.write_bytes_complete

        write_records = self.write_records

        write_records_complete = self.write_records_complete

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if accumulated_backpressured_time is not UNSET:
            field_dict["accumulated-backpressured-time"] = accumulated_backpressured_time
        if accumulated_busy_time is not UNSET:
            field_dict["accumulated-busy-time"] = accumulated_busy_time
        if accumulated_idle_time is not UNSET:
            field_dict["accumulated-idle-time"] = accumulated_idle_time
        if read_bytes is not UNSET:
            field_dict["read-bytes"] = read_bytes
        if read_bytes_complete is not UNSET:
            field_dict["read-bytes-complete"] = read_bytes_complete
        if read_records is not UNSET:
            field_dict["read-records"] = read_records
        if read_records_complete is not UNSET:
            field_dict["read-records-complete"] = read_records_complete
        if write_bytes is not UNSET:
            field_dict["write-bytes"] = write_bytes
        if write_bytes_complete is not UNSET:
            field_dict["write-bytes-complete"] = write_bytes_complete
        if write_records is not UNSET:
            field_dict["write-records"] = write_records
        if write_records_complete is not UNSET:
            field_dict["write-records-complete"] = write_records_complete

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        accumulated_backpressured_time = d.pop("accumulated-backpressured-time", UNSET)

        accumulated_busy_time = d.pop("accumulated-busy-time", UNSET)

        accumulated_idle_time = d.pop("accumulated-idle-time", UNSET)

        read_bytes = d.pop("read-bytes", UNSET)

        read_bytes_complete = d.pop("read-bytes-complete", UNSET)

        read_records = d.pop("read-records", UNSET)

        read_records_complete = d.pop("read-records-complete", UNSET)

        write_bytes = d.pop("write-bytes", UNSET)

        write_bytes_complete = d.pop("write-bytes-complete", UNSET)

        write_records = d.pop("write-records", UNSET)

        write_records_complete = d.pop("write-records-complete", UNSET)

        io_metrics_info = cls(
            accumulated_backpressured_time=accumulated_backpressured_time,
            accumulated_busy_time=accumulated_busy_time,
            accumulated_idle_time=accumulated_idle_time,
            read_bytes=read_bytes,
            read_bytes_complete=read_bytes_complete,
            read_records=read_records,
            read_records_complete=read_records_complete,
            write_bytes=write_bytes,
            write_bytes_complete=write_bytes_complete,
            write_records=write_records,
            write_records_complete=write_records_complete,
        )

        io_metrics_info.additional_properties = d
        return io_metrics_info

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
