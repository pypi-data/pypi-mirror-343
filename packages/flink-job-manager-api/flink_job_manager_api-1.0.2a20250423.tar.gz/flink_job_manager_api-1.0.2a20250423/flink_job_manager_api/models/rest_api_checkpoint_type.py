from enum import Enum


class RestAPICheckpointType(str, Enum):
    CHECKPOINT = "CHECKPOINT"
    SAVEPOINT = "SAVEPOINT"
    SYNC_SAVEPOINT = "SYNC_SAVEPOINT"
    UNALIGNED_CHECKPOINT = "UNALIGNED_CHECKPOINT"

    def __str__(self) -> str:
        return str(self.value)
