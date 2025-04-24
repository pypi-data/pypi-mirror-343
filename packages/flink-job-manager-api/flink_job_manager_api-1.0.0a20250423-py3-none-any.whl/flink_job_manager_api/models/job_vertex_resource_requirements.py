from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parallelism import Parallelism


T = TypeVar("T", bound="JobVertexResourceRequirements")


@_attrs_define
class JobVertexResourceRequirements:
    """
    Attributes:
        parallelism (Union[Unset, Parallelism]):
    """

    parallelism: Union[Unset, "Parallelism"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        parallelism: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parallelism, Unset):
            parallelism = self.parallelism.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if parallelism is not UNSET:
            field_dict["parallelism"] = parallelism

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.parallelism import Parallelism

        d = src_dict.copy()
        _parallelism = d.pop("parallelism", UNSET)
        parallelism: Union[Unset, Parallelism]
        if isinstance(_parallelism, Unset):
            parallelism = UNSET
        else:
            parallelism = Parallelism.from_dict(_parallelism)

        job_vertex_resource_requirements = cls(
            parallelism=parallelism,
        )

        job_vertex_resource_requirements.additional_properties = d
        return job_vertex_resource_requirements

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
