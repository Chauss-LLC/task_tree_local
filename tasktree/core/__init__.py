"""Core module of task_tree project."""

from random import choice
from anytree import NodeMixin
from tasktree.core.status import STATUS


class Task(NodeMixin):
    """Task class for task tree."""

    _id: int = 0

    @property
    def id(self):
        """Read-only attribute of the task."""
        return self._id

    def generate_new_id(self) -> int:
        """Generate new id for task."""
        ids: set = {t.id for t in self.root.descendants}
        return choice([i for i in range(0,10**6) if i not in ids])

    def __init__(self, name: str, status: STATUS = STATUS.PENDING, parent=None, children=None):
        """Constructor for a new Task."""
        self.name = name
        self.status = status
        self.parent = parent
        if children:
            self.children = children
        self._id = self.generate_new_id()
