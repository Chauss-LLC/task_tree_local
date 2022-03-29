"""Operations on the task status."""

from enum import Enum


class STATUS(Enum):
    """Status of the task."""

    SOLVED = 1
    PENDING = 0
    FAILED = -1
