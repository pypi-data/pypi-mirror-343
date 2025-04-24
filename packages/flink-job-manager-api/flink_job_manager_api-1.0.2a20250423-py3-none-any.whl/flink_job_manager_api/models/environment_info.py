from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.jvm_info import JVMInfo


T = TypeVar("T", bound="EnvironmentInfo")


@_attrs_define
class EnvironmentInfo:
    """
    Attributes:
        classpath (Union[Unset, list[str]]):
        jvm (Union[Unset, JVMInfo]):
    """

    classpath: Union[Unset, list[str]] = UNSET
    jvm: Union[Unset, "JVMInfo"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        classpath: Union[Unset, list[str]] = UNSET
        if not isinstance(self.classpath, Unset):
            classpath = self.classpath

        jvm: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.jvm, Unset):
            jvm = self.jvm.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if classpath is not UNSET:
            field_dict["classpath"] = classpath
        if jvm is not UNSET:
            field_dict["jvm"] = jvm

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.jvm_info import JVMInfo

        d = src_dict.copy()
        classpath = cast(list[str], d.pop("classpath", UNSET))

        _jvm = d.pop("jvm", UNSET)
        jvm: Union[Unset, JVMInfo]
        if isinstance(_jvm, Unset):
            jvm = UNSET
        else:
            jvm = JVMInfo.from_dict(_jvm)

        environment_info = cls(
            classpath=classpath,
            jvm=jvm,
        )

        environment_info.additional_properties = d
        return environment_info

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
