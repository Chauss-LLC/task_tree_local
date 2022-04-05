"""Operations on the task status."""

from enum import Enum
import emoji

class STATUS(Enum):
    """Status of the task."""

    SOLVED = 1
    PENDING = 0
    FAILED = -1

    def __str__(self):
        """Convert status to emoji."""
        emj = ""
        match self:
            case self.SOLVED:
                emj = ":check_mark_button:"
            case self.PENDING:
                emj = ":one_o’clock:"
            case self.FAILED:
                emj = ":cross_mark:"
        return emoji.emojize(emj)
