"""Connection between tasks."""

from typing import Iterable
from tasktree.core.system import TaskSystem


class Connection:
    """Connection between tasks."""

    _id: str = ""
    tags: set = set()

    CHILD_TAG: str = "child"
    PARENT_TAG: str = "parent"
    SELF_TAG: str = "self"

    def get_id(self) -> str:
        """Returns the id of a connected task."""
        return self._id

    def is_child(self) -> bool:
        """Returns True if the connection have a 'child' tag."""
        return self.have_tag(Connection.CHILD_TAG)

    def is_parent(self) -> bool:
        """Returns True if the connection have a 'parent' tag."""
        return self.have_tag(Connection.PARENT_TAG)

    def is_self(self) -> bool:
        """Returns True if the connection have a 'self' tag."""
        return self.have_tag(Connection.SELF_TAG)

    def have_tag(self, tag: str) -> bool:
        """Chack that the connection have a specified tag."""
        return tag in self.tags

    def add_tag(self, tag: str) -> bool:
        """Add unique tag. Return if the tag was added."""
        if self.have_tag(tag):
            return False
        self.tags.add(tag)
        return True

    def remove_tag(self, tag: str) -> bool:
        """Remove the tag. Return if the flag was removed."""
        if not self.have_tag(tag):
            return False
        self.tags.remove(tag)
        return True

    def __init__(self, task_id: str, tags: Iterable = []):
        """Create a new connection with task id and specified tags."""
        if len(task_id) < TaskSystem.MINIMAL_TASK_ID_LENGTH:
            raise ValueError(
                "Task id must be at least "
                f"{TaskSystem.MINIMAL_TASK_ID_LENGTH} characters length."
            )
        self._id = task_id
        self.tags = set(tags)
