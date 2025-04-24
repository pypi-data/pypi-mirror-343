from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_details_tasks import JobDetailsTasks


T = TypeVar("T", bound="JobDetails")


@_attrs_define
class JobDetails:
    """
    Attributes:
        duration (Union[Unset, int]):
        end_time (Union[Unset, int]):
        jid (Union[Unset, str]):
        last_modification (Union[Unset, int]):
        name (Union[Unset, str]):
        pending_operators (Union[Unset, int]):
        start_time (Union[Unset, int]):
        state (Union[Unset, JobStatus]):
        tasks (Union[Unset, JobDetailsTasks]):
    """

    duration: Union[Unset, int] = UNSET
    end_time: Union[Unset, int] = UNSET
    jid: Union[Unset, str] = UNSET
    last_modification: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    pending_operators: Union[Unset, int] = UNSET
    start_time: Union[Unset, int] = UNSET
    state: Union[Unset, JobStatus] = UNSET
    tasks: Union[Unset, "JobDetailsTasks"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration = self.duration

        end_time = self.end_time

        jid = self.jid

        last_modification = self.last_modification

        name = self.name

        pending_operators = self.pending_operators

        start_time = self.start_time

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        tasks: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tasks, Unset):
            tasks = self.tasks.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if duration is not UNSET:
            field_dict["duration"] = duration
        if end_time is not UNSET:
            field_dict["end-time"] = end_time
        if jid is not UNSET:
            field_dict["jid"] = jid
        if last_modification is not UNSET:
            field_dict["last-modification"] = last_modification
        if name is not UNSET:
            field_dict["name"] = name
        if pending_operators is not UNSET:
            field_dict["pending-operators"] = pending_operators
        if start_time is not UNSET:
            field_dict["start-time"] = start_time
        if state is not UNSET:
            field_dict["state"] = state
        if tasks is not UNSET:
            field_dict["tasks"] = tasks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.job_details_tasks import JobDetailsTasks

        d = src_dict.copy()
        duration = d.pop("duration", UNSET)

        end_time = d.pop("end-time", UNSET)

        jid = d.pop("jid", UNSET)

        last_modification = d.pop("last-modification", UNSET)

        name = d.pop("name", UNSET)

        pending_operators = d.pop("pending-operators", UNSET)

        start_time = d.pop("start-time", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, JobStatus]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = JobStatus(_state)

        _tasks = d.pop("tasks", UNSET)
        tasks: Union[Unset, JobDetailsTasks]
        if isinstance(_tasks, Unset):
            tasks = UNSET
        else:
            tasks = JobDetailsTasks.from_dict(_tasks)

        job_details = cls(
            duration=duration,
            end_time=end_time,
            jid=jid,
            last_modification=last_modification,
            name=name,
            pending_operators=pending_operators,
            start_time=start_time,
            state=state,
            tasks=tasks,
        )

        job_details.additional_properties = d
        return job_details

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
