from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asynchronous_operation_info import AsynchronousOperationInfo
    from ..models.checkpoint_info import CheckpointInfo
    from ..models.queue_status import QueueStatus
    from ..models.savepoint_info import SavepointInfo


T = TypeVar("T", bound="AsynchronousOperationResult")


@_attrs_define
class AsynchronousOperationResult:
    """
    Attributes:
        operation (Union['AsynchronousOperationInfo', 'CheckpointInfo', 'SavepointInfo', Unset]):
        status (Union[Unset, QueueStatus]):
    """

    operation: Union["AsynchronousOperationInfo", "CheckpointInfo", "SavepointInfo", Unset] = UNSET
    status: Union[Unset, "QueueStatus"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.asynchronous_operation_info import AsynchronousOperationInfo
        from ..models.checkpoint_info import CheckpointInfo

        operation: Union[Unset, dict[str, Any]]
        if isinstance(self.operation, Unset):
            operation = UNSET
        elif isinstance(self.operation, AsynchronousOperationInfo):
            operation = self.operation.to_dict()
        elif isinstance(self.operation, CheckpointInfo):
            operation = self.operation.to_dict()
        else:
            operation = self.operation.to_dict()

        status: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if operation is not UNSET:
            field_dict["operation"] = operation
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.asynchronous_operation_info import AsynchronousOperationInfo
        from ..models.checkpoint_info import CheckpointInfo
        from ..models.queue_status import QueueStatus
        from ..models.savepoint_info import SavepointInfo

        d = src_dict.copy()

        def _parse_operation(
            data: object,
        ) -> Union["AsynchronousOperationInfo", "CheckpointInfo", "SavepointInfo", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                operation_type_0 = AsynchronousOperationInfo.from_dict(data)

                return operation_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                operation_type_1 = CheckpointInfo.from_dict(data)

                return operation_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            operation_type_2 = SavepointInfo.from_dict(data)

            return operation_type_2

        operation = _parse_operation(d.pop("operation", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, QueueStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = QueueStatus.from_dict(_status)

        asynchronous_operation_result = cls(
            operation=operation,
            status=status,
        )

        asynchronous_operation_result.additional_properties = d
        return asynchronous_operation_result

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
