from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_accumulator import JobAccumulator
    from ..models.job_accumulators_info_serialized_user_task_accumulators import (
        JobAccumulatorsInfoSerializedUserTaskAccumulators,
    )
    from ..models.user_task_accumulator import UserTaskAccumulator


T = TypeVar("T", bound="JobAccumulatorsInfo")


@_attrs_define
class JobAccumulatorsInfo:
    """
    Attributes:
        job_accumulators (Union[Unset, list['JobAccumulator']]):
        serialized_user_task_accumulators (Union[Unset, JobAccumulatorsInfoSerializedUserTaskAccumulators]):
        user_task_accumulators (Union[Unset, list['UserTaskAccumulator']]):
    """

    job_accumulators: Union[Unset, list["JobAccumulator"]] = UNSET
    serialized_user_task_accumulators: Union[Unset, "JobAccumulatorsInfoSerializedUserTaskAccumulators"] = UNSET
    user_task_accumulators: Union[Unset, list["UserTaskAccumulator"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_accumulators: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.job_accumulators, Unset):
            job_accumulators = []
            for job_accumulators_item_data in self.job_accumulators:
                job_accumulators_item = job_accumulators_item_data.to_dict()
                job_accumulators.append(job_accumulators_item)

        serialized_user_task_accumulators: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.serialized_user_task_accumulators, Unset):
            serialized_user_task_accumulators = self.serialized_user_task_accumulators.to_dict()

        user_task_accumulators: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.user_task_accumulators, Unset):
            user_task_accumulators = []
            for user_task_accumulators_item_data in self.user_task_accumulators:
                user_task_accumulators_item = user_task_accumulators_item_data.to_dict()
                user_task_accumulators.append(user_task_accumulators_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_accumulators is not UNSET:
            field_dict["job-accumulators"] = job_accumulators
        if serialized_user_task_accumulators is not UNSET:
            field_dict["serialized-user-task-accumulators"] = serialized_user_task_accumulators
        if user_task_accumulators is not UNSET:
            field_dict["user-task-accumulators"] = user_task_accumulators

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.job_accumulator import JobAccumulator
        from ..models.job_accumulators_info_serialized_user_task_accumulators import (
            JobAccumulatorsInfoSerializedUserTaskAccumulators,
        )
        from ..models.user_task_accumulator import UserTaskAccumulator

        d = src_dict.copy()
        job_accumulators = []
        _job_accumulators = d.pop("job-accumulators", UNSET)
        for job_accumulators_item_data in _job_accumulators or []:
            job_accumulators_item = JobAccumulator.from_dict(job_accumulators_item_data)

            job_accumulators.append(job_accumulators_item)

        _serialized_user_task_accumulators = d.pop("serialized-user-task-accumulators", UNSET)
        serialized_user_task_accumulators: Union[Unset, JobAccumulatorsInfoSerializedUserTaskAccumulators]
        if isinstance(_serialized_user_task_accumulators, Unset):
            serialized_user_task_accumulators = UNSET
        else:
            serialized_user_task_accumulators = JobAccumulatorsInfoSerializedUserTaskAccumulators.from_dict(
                _serialized_user_task_accumulators
            )

        user_task_accumulators = []
        _user_task_accumulators = d.pop("user-task-accumulators", UNSET)
        for user_task_accumulators_item_data in _user_task_accumulators or []:
            user_task_accumulators_item = UserTaskAccumulator.from_dict(user_task_accumulators_item_data)

            user_task_accumulators.append(user_task_accumulators_item)

        job_accumulators_info = cls(
            job_accumulators=job_accumulators,
            serialized_user_task_accumulators=serialized_user_task_accumulators,
            user_task_accumulators=user_task_accumulators,
        )

        job_accumulators_info.additional_properties = d
        return job_accumulators_info

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
