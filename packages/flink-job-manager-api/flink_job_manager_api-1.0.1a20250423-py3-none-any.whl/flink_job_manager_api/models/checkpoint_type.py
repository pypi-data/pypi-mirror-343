from enum import Enum


class CheckpointType(str, Enum):
    CONFIGURED = "CONFIGURED"
    FULL = "FULL"
    INCREMENTAL = "INCREMENTAL"

    def __str__(self) -> str:
        return str(self.value)
