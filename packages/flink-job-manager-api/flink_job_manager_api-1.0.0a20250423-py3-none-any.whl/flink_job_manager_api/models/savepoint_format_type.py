from enum import Enum


class SavepointFormatType(str, Enum):
    CANONICAL = "CANONICAL"
    NATIVE = "NATIVE"

    def __str__(self) -> str:
        return str(self.value)
