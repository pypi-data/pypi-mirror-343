from enum import Enum


class ProcessingMode(str, Enum):
    AT_LEAST_ONCE = "AT_LEAST_ONCE"
    EXACTLY_ONCE = "EXACTLY_ONCE"

    def __str__(self) -> str:
        return str(self.value)
