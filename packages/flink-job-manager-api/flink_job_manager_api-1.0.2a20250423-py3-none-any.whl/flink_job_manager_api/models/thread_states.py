from enum import Enum


class ThreadStates(str, Enum):
    FULL = "FULL"
    OFF_CPU = "OFF_CPU"
    ON_CPU = "ON_CPU"

    def __str__(self) -> str:
        return str(self.value)
