from enum import Enum


class ExecutionState(str, Enum):
    CANCELED = "CANCELED"
    CANCELING = "CANCELING"
    CREATED = "CREATED"
    DEPLOYING = "DEPLOYING"
    FAILED = "FAILED"
    FINISHED = "FINISHED"
    INITIALIZING = "INITIALIZING"
    RECONCILING = "RECONCILING"
    RUNNING = "RUNNING"
    SCHEDULED = "SCHEDULED"

    def __str__(self) -> str:
        return str(self.value)
