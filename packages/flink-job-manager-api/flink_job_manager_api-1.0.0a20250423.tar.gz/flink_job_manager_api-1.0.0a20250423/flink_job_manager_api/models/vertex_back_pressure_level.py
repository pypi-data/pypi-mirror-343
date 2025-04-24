from enum import Enum


class VertexBackPressureLevel(str, Enum):
    HIGH = "high"
    LOW = "low"
    OK = "ok"

    def __str__(self) -> str:
        return str(self.value)
