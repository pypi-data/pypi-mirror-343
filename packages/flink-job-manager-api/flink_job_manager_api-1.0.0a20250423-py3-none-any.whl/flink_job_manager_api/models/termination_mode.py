from enum import Enum


class TerminationMode(str, Enum):
    CANCEL = "CANCEL"
    STOP = "STOP"

    def __str__(self) -> str:
        return str(self.value)
