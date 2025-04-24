from enum import Enum


class JobStatus(str, Enum):
    CANCELED = "CANCELED"
    CANCELLING = "CANCELLING"
    CREATED = "CREATED"
    FAILED = "FAILED"
    FAILING = "FAILING"
    FINISHED = "FINISHED"
    INITIALIZING = "INITIALIZING"
    RECONCILING = "RECONCILING"
    RESTARTING = "RESTARTING"
    RUNNING = "RUNNING"
    SUSPENDED = "SUSPENDED"

    def __str__(self) -> str:
        return str(self.value)
