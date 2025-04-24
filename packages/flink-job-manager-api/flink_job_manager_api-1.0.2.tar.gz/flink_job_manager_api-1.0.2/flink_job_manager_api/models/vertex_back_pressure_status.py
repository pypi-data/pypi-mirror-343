from enum import Enum


class VertexBackPressureStatus(str, Enum):
    DEPRECATED = "deprecated"
    OK = "ok"

    def __str__(self) -> str:
        return str(self.value)
