"""Core module of task_tree project."""

from anytree import NodeMixin
from tasktree.core.status import STATUS

class Task(NodeMixin):
    """Task class for task tree."""

    def __init__(self, name, status: STATUS = STATUS.PENDING, parent=None, children=None):
        """Constructor for a new Task."""
        self.name = name
        self.status = status
        self.parent = parent
        if children:
            self.children = children
