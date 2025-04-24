from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_exception_history import JobExceptionHistory


T = TypeVar("T", bound="JobExceptionsInfoWithHistory")


@_attrs_define
class JobExceptionsInfoWithHistory:
    """
    Attributes:
        exception_history (Union[Unset, JobExceptionHistory]):
    """

    exception_history: Union[Unset, "JobExceptionHistory"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        exception_history: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.exception_history, Unset):
            exception_history = self.exception_history.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if exception_history is not UNSET:
            field_dict["exceptionHistory"] = exception_history

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.job_exception_history import JobExceptionHistory

        d = src_dict.copy()
        _exception_history = d.pop("exceptionHistory", UNSET)
        exception_history: Union[Unset, JobExceptionHistory]
        if isinstance(_exception_history, Unset):
            exception_history = UNSET
        else:
            exception_history = JobExceptionHistory.from_dict(_exception_history)

        job_exceptions_info_with_history = cls(
            exception_history=exception_history,
        )

        job_exceptions_info_with_history.additional_properties = d
        return job_exceptions_info_with_history

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
