from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.processing_mode import ProcessingMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.externalized_checkpoint_info import ExternalizedCheckpointInfo


T = TypeVar("T", bound="CheckpointConfigInfo")


@_attrs_define
class CheckpointConfigInfo:
    """
    Attributes:
        aligned_checkpoint_timeout (Union[Unset, int]):
        changelog_periodic_materialization_interval (Union[Unset, int]):
        changelog_storage (Union[Unset, str]):
        checkpoint_storage (Union[Unset, str]):
        checkpoints_after_tasks_finish (Union[Unset, bool]):
        externalization (Union[Unset, ExternalizedCheckpointInfo]):
        interval (Union[Unset, int]):
        max_concurrent (Union[Unset, int]):
        min_pause (Union[Unset, int]):
        mode (Union[Unset, ProcessingMode]):
        state_backend (Union[Unset, str]):
        state_changelog_enabled (Union[Unset, bool]):
        timeout (Union[Unset, int]):
        tolerable_failed_checkpoints (Union[Unset, int]):
        unaligned_checkpoints (Union[Unset, bool]):
    """

    aligned_checkpoint_timeout: Union[Unset, int] = UNSET
    changelog_periodic_materialization_interval: Union[Unset, int] = UNSET
    changelog_storage: Union[Unset, str] = UNSET
    checkpoint_storage: Union[Unset, str] = UNSET
    checkpoints_after_tasks_finish: Union[Unset, bool] = UNSET
    externalization: Union[Unset, "ExternalizedCheckpointInfo"] = UNSET
    interval: Union[Unset, int] = UNSET
    max_concurrent: Union[Unset, int] = UNSET
    min_pause: Union[Unset, int] = UNSET
    mode: Union[Unset, ProcessingMode] = UNSET
    state_backend: Union[Unset, str] = UNSET
    state_changelog_enabled: Union[Unset, bool] = UNSET
    timeout: Union[Unset, int] = UNSET
    tolerable_failed_checkpoints: Union[Unset, int] = UNSET
    unaligned_checkpoints: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        aligned_checkpoint_timeout = self.aligned_checkpoint_timeout

        changelog_periodic_materialization_interval = self.changelog_periodic_materialization_interval

        changelog_storage = self.changelog_storage

        checkpoint_storage = self.checkpoint_storage

        checkpoints_after_tasks_finish = self.checkpoints_after_tasks_finish

        externalization: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.externalization, Unset):
            externalization = self.externalization.to_dict()

        interval = self.interval

        max_concurrent = self.max_concurrent

        min_pause = self.min_pause

        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        state_backend = self.state_backend

        state_changelog_enabled = self.state_changelog_enabled

        timeout = self.timeout

        tolerable_failed_checkpoints = self.tolerable_failed_checkpoints

        unaligned_checkpoints = self.unaligned_checkpoints

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aligned_checkpoint_timeout is not UNSET:
            field_dict["aligned_checkpoint_timeout"] = aligned_checkpoint_timeout
        if changelog_periodic_materialization_interval is not UNSET:
            field_dict["changelog_periodic_materialization_interval"] = changelog_periodic_materialization_interval
        if changelog_storage is not UNSET:
            field_dict["changelog_storage"] = changelog_storage
        if checkpoint_storage is not UNSET:
            field_dict["checkpoint_storage"] = checkpoint_storage
        if checkpoints_after_tasks_finish is not UNSET:
            field_dict["checkpoints_after_tasks_finish"] = checkpoints_after_tasks_finish
        if externalization is not UNSET:
            field_dict["externalization"] = externalization
        if interval is not UNSET:
            field_dict["interval"] = interval
        if max_concurrent is not UNSET:
            field_dict["max_concurrent"] = max_concurrent
        if min_pause is not UNSET:
            field_dict["min_pause"] = min_pause
        if mode is not UNSET:
            field_dict["mode"] = mode
        if state_backend is not UNSET:
            field_dict["state_backend"] = state_backend
        if state_changelog_enabled is not UNSET:
            field_dict["state_changelog_enabled"] = state_changelog_enabled
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if tolerable_failed_checkpoints is not UNSET:
            field_dict["tolerable_failed_checkpoints"] = tolerable_failed_checkpoints
        if unaligned_checkpoints is not UNSET:
            field_dict["unaligned_checkpoints"] = unaligned_checkpoints

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.externalized_checkpoint_info import ExternalizedCheckpointInfo

        d = src_dict.copy()
        aligned_checkpoint_timeout = d.pop("aligned_checkpoint_timeout", UNSET)

        changelog_periodic_materialization_interval = d.pop("changelog_periodic_materialization_interval", UNSET)

        changelog_storage = d.pop("changelog_storage", UNSET)

        checkpoint_storage = d.pop("checkpoint_storage", UNSET)

        checkpoints_after_tasks_finish = d.pop("checkpoints_after_tasks_finish", UNSET)

        _externalization = d.pop("externalization", UNSET)
        externalization: Union[Unset, ExternalizedCheckpointInfo]
        if isinstance(_externalization, Unset):
            externalization = UNSET
        else:
            externalization = ExternalizedCheckpointInfo.from_dict(_externalization)

        interval = d.pop("interval", UNSET)

        max_concurrent = d.pop("max_concurrent", UNSET)

        min_pause = d.pop("min_pause", UNSET)

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, ProcessingMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = ProcessingMode(_mode)

        state_backend = d.pop("state_backend", UNSET)

        state_changelog_enabled = d.pop("state_changelog_enabled", UNSET)

        timeout = d.pop("timeout", UNSET)

        tolerable_failed_checkpoints = d.pop("tolerable_failed_checkpoints", UNSET)

        unaligned_checkpoints = d.pop("unaligned_checkpoints", UNSET)

        checkpoint_config_info = cls(
            aligned_checkpoint_timeout=aligned_checkpoint_timeout,
            changelog_periodic_materialization_interval=changelog_periodic_materialization_interval,
            changelog_storage=changelog_storage,
            checkpoint_storage=checkpoint_storage,
            checkpoints_after_tasks_finish=checkpoints_after_tasks_finish,
            externalization=externalization,
            interval=interval,
            max_concurrent=max_concurrent,
            min_pause=min_pause,
            mode=mode,
            state_backend=state_backend,
            state_changelog_enabled=state_changelog_enabled,
            timeout=timeout,
            tolerable_failed_checkpoints=tolerable_failed_checkpoints,
            unaligned_checkpoints=unaligned_checkpoints,
        )

        checkpoint_config_info.additional_properties = d
        return checkpoint_config_info

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
