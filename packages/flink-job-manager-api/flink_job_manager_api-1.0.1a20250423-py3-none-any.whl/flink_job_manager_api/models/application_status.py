from enum import Enum


class ApplicationStatus(str, Enum):
    CANCELED = "CANCELED"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)
