"""System of tasks."""

import random
import string


class IdReadOnlyDescriptor:
    """Descriptor for id field, so you can not modify id of the established connection."""

    def __get__(self, obj, cls):
        """Returns the id."""
        return obj._id_field

    def __set__(self, obj, val):
        """Sets the id. Works only once for each object."""
        if hasattr(obj, '_id_set') and obj._id_set:
            raise TypeError(f"'{type(obj).__name__}' object does not support id assignment")
        obj._id_field = val
        obj._id_set = True

class TaskSystem:
    """Control the system of tasks."""

    IdType = str
    MINIMAL_TASK_ID_LENGTH = 6

    def is_task_id_correct(self=None, task_id: IdType = IdType()) -> bool:
        """Check if task id is correct (allow to discard some ids)."""
        return len(task_id) >= TaskSystem.MINIMAL_TASK_ID_LENGTH

    def generate_task_id(self=None) -> IdType:
        """Generate random task id."""
        allowed_characters = set(string.ascii_lowercase + string.digits)
        return "".join(
            random.choices(allowed_characters, k=TaskSystem.MINIMAL_TASK_ID_LENGTH)
        )
