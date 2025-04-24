from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.exception_info import ExceptionInfo
    from ..models.root_exception_info_failure_labels import RootExceptionInfoFailureLabels


T = TypeVar("T", bound="RootExceptionInfo")


@_attrs_define
class RootExceptionInfo:
    """
    Attributes:
        concurrent_exceptions (Union[Unset, list['ExceptionInfo']]):
        endpoint (Union[Unset, str]):
        exception_name (Union[Unset, str]):
        failure_labels (Union[Unset, RootExceptionInfoFailureLabels]):
        stacktrace (Union[Unset, str]):
        task_manager_id (Union[Unset, str]):
        task_name (Union[Unset, str]):
        timestamp (Union[Unset, int]):
    """

    concurrent_exceptions: Union[Unset, list["ExceptionInfo"]] = UNSET
    endpoint: Union[Unset, str] = UNSET
    exception_name: Union[Unset, str] = UNSET
    failure_labels: Union[Unset, "RootExceptionInfoFailureLabels"] = UNSET
    stacktrace: Union[Unset, str] = UNSET
    task_manager_id: Union[Unset, str] = UNSET
    task_name: Union[Unset, str] = UNSET
    timestamp: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        concurrent_exceptions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.concurrent_exceptions, Unset):
            concurrent_exceptions = []
            for concurrent_exceptions_item_data in self.concurrent_exceptions:
                concurrent_exceptions_item = concurrent_exceptions_item_data.to_dict()
                concurrent_exceptions.append(concurrent_exceptions_item)

        endpoint = self.endpoint

        exception_name = self.exception_name

        failure_labels: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.failure_labels, Unset):
            failure_labels = self.failure_labels.to_dict()

        stacktrace = self.stacktrace

        task_manager_id = self.task_manager_id

        task_name = self.task_name

        timestamp = self.timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if concurrent_exceptions is not UNSET:
            field_dict["concurrentExceptions"] = concurrent_exceptions
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if exception_name is not UNSET:
            field_dict["exceptionName"] = exception_name
        if failure_labels is not UNSET:
            field_dict["failureLabels"] = failure_labels
        if stacktrace is not UNSET:
            field_dict["stacktrace"] = stacktrace
        if task_manager_id is not UNSET:
            field_dict["taskManagerId"] = task_manager_id
        if task_name is not UNSET:
            field_dict["taskName"] = task_name
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.exception_info import ExceptionInfo
        from ..models.root_exception_info_failure_labels import RootExceptionInfoFailureLabels

        d = src_dict.copy()
        concurrent_exceptions = []
        _concurrent_exceptions = d.pop("concurrentExceptions", UNSET)
        for concurrent_exceptions_item_data in _concurrent_exceptions or []:
            concurrent_exceptions_item = ExceptionInfo.from_dict(concurrent_exceptions_item_data)

            concurrent_exceptions.append(concurrent_exceptions_item)

        endpoint = d.pop("endpoint", UNSET)

        exception_name = d.pop("exceptionName", UNSET)

        _failure_labels = d.pop("failureLabels", UNSET)
        failure_labels: Union[Unset, RootExceptionInfoFailureLabels]
        if isinstance(_failure_labels, Unset):
            failure_labels = UNSET
        else:
            failure_labels = RootExceptionInfoFailureLabels.from_dict(_failure_labels)

        stacktrace = d.pop("stacktrace", UNSET)

        task_manager_id = d.pop("taskManagerId", UNSET)

        task_name = d.pop("taskName", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        root_exception_info = cls(
            concurrent_exceptions=concurrent_exceptions,
            endpoint=endpoint,
            exception_name=exception_name,
            failure_labels=failure_labels,
            stacktrace=stacktrace,
            task_manager_id=task_manager_id,
            task_name=task_name,
            timestamp=timestamp,
        )

        root_exception_info.additional_properties = d
        return root_exception_info

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
