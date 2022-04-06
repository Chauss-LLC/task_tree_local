"""Core module of task_tree project."""

from random import choice
from anytree import NodeMixin
from tasktree.core.status import STATUS
from termcolor import colored


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

    def remove_child_by_id(self, id: int) -> bool:
        """Remove a child from Task by id. Return true if the child was removed."""
        if id in {t.id for t in self.children}:
            self.children = (t for t in self.children if t.id != id)
            return True
        return False

    def remove_child(self, child) -> bool:
        """Remove a child from Task by object."""
        return self.remove_child_by_id(child.id)

    def __str__(self):
        """Return a string representation of the Task."""
        return str(self.status) + " " + self.name + " " + colored(f"(#{str(self.id)})", 'cyan')

    def __repr__(self):
        return f"Task({int(self.status)}, {self.name}, #{self.id})"
