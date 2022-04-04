"""Module with mplementation of pickle storage."""
import pickle

from tasktree.store.base_store import BaseStore
from tasktree.core import Task


class PickleStore(BaseStore):
    """
    Class for store task tree in pickle format.

    :param path: Path to .pickle file
    :type path: str
    """

    def __init__(self, path):
        """Remember path to storage file."""
        self.path = path
        self.file = None

    def __enter__(self):
        """Open pickle file."""
        self.file = open(self.path, 'r+b')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close pickle file."""
        self.file.close()
        self.file = None

    def get_tree(self, tid: int = None) -> Task:
        """
        Return root of stored tree.

        :param tid: Optional tree root id for retrieving
        :type tid: int
        :return: Root of stored tree
        :rtype: Task
        """
        try:
            task = pickle.load(self.file)
        except TypeError as err:
            raise ValueError("File wasn't open") from err
        self.file.seek(0)
        if tid is not None:
            task = task.findby(tid=tid)
        return task

    def save_tree(self, root: Task):
        """
        Save tree by given root.

        :param root: Root task of saveing tree
        :type root: Task
        """
        try:
            pickle.dump(root, self.file)
        except TypeError as err:
            raise ValueError("File wasn't open") from err
        self.file.seek(0)
