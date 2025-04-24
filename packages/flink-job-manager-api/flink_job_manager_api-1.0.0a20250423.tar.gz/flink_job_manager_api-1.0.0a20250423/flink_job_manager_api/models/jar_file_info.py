from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.jar_entry_info import JarEntryInfo


T = TypeVar("T", bound="JarFileInfo")


@_attrs_define
class JarFileInfo:
    """
    Attributes:
        entry (Union[Unset, list['JarEntryInfo']]):
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        uploaded (Union[Unset, int]):
    """

    entry: Union[Unset, list["JarEntryInfo"]] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    uploaded: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entry: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.entry, Unset):
            entry = []
            for entry_item_data in self.entry:
                entry_item = entry_item_data.to_dict()
                entry.append(entry_item)

        id = self.id

        name = self.name

        uploaded = self.uploaded

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if entry is not UNSET:
            field_dict["entry"] = entry
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if uploaded is not UNSET:
            field_dict["uploaded"] = uploaded

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.jar_entry_info import JarEntryInfo

        d = src_dict.copy()
        entry = []
        _entry = d.pop("entry", UNSET)
        for entry_item_data in _entry or []:
            entry_item = JarEntryInfo.from_dict(entry_item_data)

            entry.append(entry_item)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        uploaded = d.pop("uploaded", UNSET)

        jar_file_info = cls(
            entry=entry,
            id=id,
            name=name,
            uploaded=uploaded,
        )

        jar_file_info.additional_properties = d
        return jar_file_info

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
