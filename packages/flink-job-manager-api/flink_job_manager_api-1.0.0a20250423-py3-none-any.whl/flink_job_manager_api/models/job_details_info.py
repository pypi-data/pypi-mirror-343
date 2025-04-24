from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..models.job_type import JobType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_details_info_status_counts import JobDetailsInfoStatusCounts
    from ..models.job_details_info_timestamps import JobDetailsInfoTimestamps
    from ..models.job_details_vertex_info import JobDetailsVertexInfo
    from ..models.plan import Plan
    from ..models.raw_json import RawJson


T = TypeVar("T", bound="JobDetailsInfo")


@_attrs_define
class JobDetailsInfo:
    """
    Attributes:
        duration (Union[Unset, int]):
        end_time (Union[Unset, int]):
        is_stoppable (Union[Unset, bool]):
        jid (Union[Unset, str]):
        job_type (Union[Unset, JobType]):
        max_parallelism (Union[Unset, int]):
        name (Union[Unset, str]):
        now (Union[Unset, int]):
        pending_operators (Union[Unset, int]):
        plan (Union[Unset, Plan]):
        start_time (Union[Unset, int]):
        state (Union[Unset, JobStatus]):
        status_counts (Union[Unset, JobDetailsInfoStatusCounts]):
        stream_graph (Union[Unset, RawJson]):
        timestamps (Union[Unset, JobDetailsInfoTimestamps]):
        vertices (Union[Unset, list['JobDetailsVertexInfo']]):
    """

    duration: Union[Unset, int] = UNSET
    end_time: Union[Unset, int] = UNSET
    is_stoppable: Union[Unset, bool] = UNSET
    jid: Union[Unset, str] = UNSET
    job_type: Union[Unset, JobType] = UNSET
    max_parallelism: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    now: Union[Unset, int] = UNSET
    pending_operators: Union[Unset, int] = UNSET
    plan: Union[Unset, "Plan"] = UNSET
    start_time: Union[Unset, int] = UNSET
    state: Union[Unset, JobStatus] = UNSET
    status_counts: Union[Unset, "JobDetailsInfoStatusCounts"] = UNSET
    stream_graph: Union[Unset, "RawJson"] = UNSET
    timestamps: Union[Unset, "JobDetailsInfoTimestamps"] = UNSET
    vertices: Union[Unset, list["JobDetailsVertexInfo"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration = self.duration

        end_time = self.end_time

        is_stoppable = self.is_stoppable

        jid = self.jid

        job_type: Union[Unset, str] = UNSET
        if not isinstance(self.job_type, Unset):
            job_type = self.job_type.value

        max_parallelism = self.max_parallelism

        name = self.name

        now = self.now

        pending_operators = self.pending_operators

        plan: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.to_dict()

        start_time = self.start_time

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        status_counts: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.status_counts, Unset):
            status_counts = self.status_counts.to_dict()

        stream_graph: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.stream_graph, Unset):
            stream_graph = self.stream_graph.to_dict()

        timestamps: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.timestamps, Unset):
            timestamps = self.timestamps.to_dict()

        vertices: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.vertices, Unset):
            vertices = []
            for vertices_item_data in self.vertices:
                vertices_item = vertices_item_data.to_dict()
                vertices.append(vertices_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if duration is not UNSET:
            field_dict["duration"] = duration
        if end_time is not UNSET:
            field_dict["end-time"] = end_time
        if is_stoppable is not UNSET:
            field_dict["isStoppable"] = is_stoppable
        if jid is not UNSET:
            field_dict["jid"] = jid
        if job_type is not UNSET:
            field_dict["job-type"] = job_type
        if max_parallelism is not UNSET:
            field_dict["maxParallelism"] = max_parallelism
        if name is not UNSET:
            field_dict["name"] = name
        if now is not UNSET:
            field_dict["now"] = now
        if pending_operators is not UNSET:
            field_dict["pending-operators"] = pending_operators
        if plan is not UNSET:
            field_dict["plan"] = plan
        if start_time is not UNSET:
            field_dict["start-time"] = start_time
        if state is not UNSET:
            field_dict["state"] = state
        if status_counts is not UNSET:
            field_dict["status-counts"] = status_counts
        if stream_graph is not UNSET:
            field_dict["stream-graph"] = stream_graph
        if timestamps is not UNSET:
            field_dict["timestamps"] = timestamps
        if vertices is not UNSET:
            field_dict["vertices"] = vertices

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.job_details_info_status_counts import JobDetailsInfoStatusCounts
        from ..models.job_details_info_timestamps import JobDetailsInfoTimestamps
        from ..models.job_details_vertex_info import JobDetailsVertexInfo
        from ..models.plan import Plan
        from ..models.raw_json import RawJson

        d = src_dict.copy()
        duration = d.pop("duration", UNSET)

        end_time = d.pop("end-time", UNSET)

        is_stoppable = d.pop("isStoppable", UNSET)

        jid = d.pop("jid", UNSET)

        _job_type = d.pop("job-type", UNSET)
        job_type: Union[Unset, JobType]
        if isinstance(_job_type, Unset):
            job_type = UNSET
        else:
            job_type = JobType(_job_type)

        max_parallelism = d.pop("maxParallelism", UNSET)

        name = d.pop("name", UNSET)

        now = d.pop("now", UNSET)

        pending_operators = d.pop("pending-operators", UNSET)

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, Plan]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = Plan.from_dict(_plan)

        start_time = d.pop("start-time", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, JobStatus]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = JobStatus(_state)

        _status_counts = d.pop("status-counts", UNSET)
        status_counts: Union[Unset, JobDetailsInfoStatusCounts]
        if isinstance(_status_counts, Unset):
            status_counts = UNSET
        else:
            status_counts = JobDetailsInfoStatusCounts.from_dict(_status_counts)

        _stream_graph = d.pop("stream-graph", UNSET)
        stream_graph: Union[Unset, RawJson]
        if isinstance(_stream_graph, Unset):
            stream_graph = UNSET
        else:
            stream_graph = RawJson.from_dict(_stream_graph)

        _timestamps = d.pop("timestamps", UNSET)
        timestamps: Union[Unset, JobDetailsInfoTimestamps]
        if isinstance(_timestamps, Unset):
            timestamps = UNSET
        else:
            timestamps = JobDetailsInfoTimestamps.from_dict(_timestamps)

        vertices = []
        _vertices = d.pop("vertices", UNSET)
        for vertices_item_data in _vertices or []:
            vertices_item = JobDetailsVertexInfo.from_dict(vertices_item_data)

            vertices.append(vertices_item)

        job_details_info = cls(
            duration=duration,
            end_time=end_time,
            is_stoppable=is_stoppable,
            jid=jid,
            job_type=job_type,
            max_parallelism=max_parallelism,
            name=name,
            now=now,
            pending_operators=pending_operators,
            plan=plan,
            start_time=start_time,
            state=state,
            status_counts=status_counts,
            stream_graph=stream_graph,
            timestamps=timestamps,
            vertices=vertices,
        )

        job_details_info.additional_properties = d
        return job_details_info

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
