"""Module with BaseStore interface."""
from tasktree.core import Task


class BaseStore:
    """Base class for different store implementations."""

    def __enter__(self):
        """Execute before context. Open necessary files/connections."""
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Execute after context. Close opened files/connections."""
        raise NotImplementedError

    def get_tree(self, tid: int = 0) -> Task:
        """
        Return root of stored tree.

        :param tid: Optional tree root id for retrieving
        :type tid: int
        :return: Root of stored tree
        :rtype: Task
        """
        raise NotImplementedError

    def save_tree(self, root: Task):
        """
        Save tree by given root.

        :param root: Root task of saveing tree
        :type root: Task
        """
        raise NotImplementedError
