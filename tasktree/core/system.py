"""System of tasks."""

import random
import string


class TaskSystem:
    """Control the system of tasks."""

    MINIMAL_TASK_ID_LENGTH = 6

    def genrate_task_id(self=None) -> str:
        """Generate random task id."""
        allowed_characters = set(string.ascii_lowercase + string.digits)
        return "".join(
            random.choices(allowed_characters, k=TaskSystem.MINIMAL_TASK_ID_LENGTH)
        )
