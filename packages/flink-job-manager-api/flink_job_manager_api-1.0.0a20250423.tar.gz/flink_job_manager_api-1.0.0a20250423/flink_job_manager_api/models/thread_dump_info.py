from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.thread_info import ThreadInfo


T = TypeVar("T", bound="ThreadDumpInfo")


@_attrs_define
class ThreadDumpInfo:
    """
    Attributes:
        thread_infos (Union[Unset, list['ThreadInfo']]):
    """

    thread_infos: Union[Unset, list["ThreadInfo"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thread_infos: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.thread_infos, Unset):
            thread_infos = []
            for thread_infos_item_data in self.thread_infos:
                thread_infos_item = thread_infos_item_data.to_dict()
                thread_infos.append(thread_infos_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if thread_infos is not UNSET:
            field_dict["threadInfos"] = thread_infos

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.thread_info import ThreadInfo

        d = src_dict.copy()
        thread_infos = []
        _thread_infos = d.pop("threadInfos", UNSET)
        for thread_infos_item_data in _thread_infos or []:
            thread_infos_item = ThreadInfo.from_dict(thread_infos_item_data)

            thread_infos.append(thread_infos_item)

        thread_dump_info = cls(
            thread_infos=thread_infos,
        )

        thread_dump_info.additional_properties = d
        return thread_dump_info

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
