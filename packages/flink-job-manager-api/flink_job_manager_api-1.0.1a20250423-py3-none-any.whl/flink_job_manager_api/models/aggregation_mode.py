from enum import Enum


class AggregationMode(str, Enum):
    AVG = "AVG"
    MAX = "MAX"
    MIN = "MIN"
    SKEW = "SKEW"
    SUM = "SUM"

    def __str__(self) -> str:
        return str(self.value)
