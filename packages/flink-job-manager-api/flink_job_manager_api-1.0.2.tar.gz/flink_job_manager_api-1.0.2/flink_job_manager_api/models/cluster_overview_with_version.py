from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ClusterOverviewWithVersion")


@_attrs_define
class ClusterOverviewWithVersion:
    """
    Attributes:
        flink_commit (Union[Unset, str]):
        flink_version (Union[Unset, str]):
        jobs_cancelled (Union[Unset, int]):
        jobs_failed (Union[Unset, int]):
        jobs_finished (Union[Unset, int]):
        jobs_running (Union[Unset, int]):
        slots_available (Union[Unset, int]):
        slots_free_and_blocked (Union[Unset, int]):
        slots_total (Union[Unset, int]):
        taskmanagers (Union[Unset, int]):
        taskmanagers_blocked (Union[Unset, int]):
    """

    flink_commit: Union[Unset, str] = UNSET
    flink_version: Union[Unset, str] = UNSET
    jobs_cancelled: Union[Unset, int] = UNSET
    jobs_failed: Union[Unset, int] = UNSET
    jobs_finished: Union[Unset, int] = UNSET
    jobs_running: Union[Unset, int] = UNSET
    slots_available: Union[Unset, int] = UNSET
    slots_free_and_blocked: Union[Unset, int] = UNSET
    slots_total: Union[Unset, int] = UNSET
    taskmanagers: Union[Unset, int] = UNSET
    taskmanagers_blocked: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flink_commit = self.flink_commit

        flink_version = self.flink_version

        jobs_cancelled = self.jobs_cancelled

        jobs_failed = self.jobs_failed

        jobs_finished = self.jobs_finished

        jobs_running = self.jobs_running

        slots_available = self.slots_available

        slots_free_and_blocked = self.slots_free_and_blocked

        slots_total = self.slots_total

        taskmanagers = self.taskmanagers

        taskmanagers_blocked = self.taskmanagers_blocked

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if flink_commit is not UNSET:
            field_dict["flink-commit"] = flink_commit
        if flink_version is not UNSET:
            field_dict["flink-version"] = flink_version
        if jobs_cancelled is not UNSET:
            field_dict["jobs-cancelled"] = jobs_cancelled
        if jobs_failed is not UNSET:
            field_dict["jobs-failed"] = jobs_failed
        if jobs_finished is not UNSET:
            field_dict["jobs-finished"] = jobs_finished
        if jobs_running is not UNSET:
            field_dict["jobs-running"] = jobs_running
        if slots_available is not UNSET:
            field_dict["slots-available"] = slots_available
        if slots_free_and_blocked is not UNSET:
            field_dict["slots-free-and-blocked"] = slots_free_and_blocked
        if slots_total is not UNSET:
            field_dict["slots-total"] = slots_total
        if taskmanagers is not UNSET:
            field_dict["taskmanagers"] = taskmanagers
        if taskmanagers_blocked is not UNSET:
            field_dict["taskmanagers-blocked"] = taskmanagers_blocked

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        flink_commit = d.pop("flink-commit", UNSET)

        flink_version = d.pop("flink-version", UNSET)

        jobs_cancelled = d.pop("jobs-cancelled", UNSET)

        jobs_failed = d.pop("jobs-failed", UNSET)

        jobs_finished = d.pop("jobs-finished", UNSET)

        jobs_running = d.pop("jobs-running", UNSET)

        slots_available = d.pop("slots-available", UNSET)

        slots_free_and_blocked = d.pop("slots-free-and-blocked", UNSET)

        slots_total = d.pop("slots-total", UNSET)

        taskmanagers = d.pop("taskmanagers", UNSET)

        taskmanagers_blocked = d.pop("taskmanagers-blocked", UNSET)

        cluster_overview_with_version = cls(
            flink_commit=flink_commit,
            flink_version=flink_version,
            jobs_cancelled=jobs_cancelled,
            jobs_failed=jobs_failed,
            jobs_finished=jobs_finished,
            jobs_running=jobs_running,
            slots_available=slots_available,
            slots_free_and_blocked=slots_free_and_blocked,
            slots_total=slots_total,
            taskmanagers=taskmanagers,
            taskmanagers_blocked=taskmanagers_blocked,
        )

        cluster_overview_with_version.additional_properties = d
        return cluster_overview_with_version

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
