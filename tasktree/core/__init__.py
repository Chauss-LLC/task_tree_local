"""Core module of task_tree project."""

from anytree import NodeMixin

class Task(NodeMixin):
    """Task class for task tree."""

    def __init__(self, name, status, parent=None, children=None):
        """Constructor for a new Task."""
        self.name = name
        self.status = status
        self.parent = parent
        if children:
            self.children = children
