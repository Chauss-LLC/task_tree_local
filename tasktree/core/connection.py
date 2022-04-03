"""Connection between tasks."""

import re
from typing import Iterable
from tasktree.core.system import TaskSystem

IdType = TaskSystem.IdType

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

class Connection:
    """Connection between tasks."""

    """Id of the connection. Do not modify, create new Connection instead."""
    _id: IdType = IdReadOnlyDescriptor()

    tags: set = set()

    CHILD_TAG: str = "child"
    PARENT_TAG: str = "parent"
    SELF_TAG: str = "self"
  
    def __check_task_id(self, task_id: IdType):
        """Check if task id is correct and raise exception on failure."""
        if not TaskSystem.is_task_id_correct(task_id=task_id):
            raise ValueError(
                "Task id was discarded by TaskSystem."
            )

    def __init__(self, task_id: IdType, tags: Iterable = []):
        """Create a new connection with task id and specified tags."""
        self.__check_task_id(task_id)
        self._id = task_id
        self.tags = set(tags)

    def copy(self, new_task_id: IdType):
        """Create new Connection with the same tags. Do not pass the same id to it."""
        if self._id == new_task_id:
            raise ValueError("You used the same task id to create a new Connection. Consider change 'tags'-field.")
        return Connection(new_task_id, self.tags)

    def get_id(self) -> IdType:
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

    def fullmatch_any_tag(self, tag_patten: str) -> bool:
        """Returns true if any of tags fully matches the regex pattern."""
        for tag in self.tags:
            if re.fullmatch(tag_patten, tag) is not None:
                return True
        return False

    def __hash__(self) -> int:
        """Return hash of the connection."""
        return hash(self._id)

    def __eq__(self, other) -> bool:
        """Compare 2 connetions object for equivalence."""
        if not isinstance(other, type(self)): return NotImplemented
        return self._id == other._id
    
    def __ne__(self, other) -> bool:
        """Compare 2 connetions object for not equivalence."""
        if not isinstance(other, type(self)): return NotImplemented
        return self._id != other._id
