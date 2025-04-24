from enum import Enum


class RecoveryClaimMode(str, Enum):
    CLAIM = "CLAIM"
    LEGACY = "LEGACY"
    NO_CLAIM = "NO_CLAIM"

    def __str__(self) -> str:
        return str(self.value)
