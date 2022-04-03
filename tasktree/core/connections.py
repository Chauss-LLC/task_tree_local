"""Store connections in one data type."""

import json
from itertools import tee
from typing import Generator, Iterable, Iterator, Set
import tasktree.core.connection as c

IdType = str

class Connections:
    """Class for storing and manipulating connection objects."""

    data: Set[c.Connection] = set()

    def __init__(self, connections: Iterable = [], self_id: IdType = None):
        """Create new data structure for connection objects.
        
        If self_id is not None create connection to self.
        Behavior is undefined if connections argument have some connection objects that have the same id.
        """
        connections = Connections.__check_iterable_have_only_connections(connections)
        self.data = set(connections)
        if self_id is not None:
            self.data.add(c.Connection(self_id, ["self", "guard"]))

    def find_connection(self, search_id: IdType) -> c.Connection:
        """Find a connection object by task id or return None on failure."""
        try:
            connection = next(filter(lambda x: x._id == search_id, self.data))
            return connection
        except StopIteration:
            return None

    def ids(self) -> Generator:
        """Return a generator over connected task ids."""
        for connection in self.data:
            yield connection.get_id()

    def with_tag(self, search_tag: str) -> Generator:
        """Return a generator over connections that have a specified tag."""
        for connection in self.data:
            if connection.have_tag(search_tag):
                yield connection

    def match_tag(self, tag_pattern: str) -> Generator:
        """Return a generator over connections that have at least one tag that fully matches given regex pattern."""
        for connection in self.data:
            if connection.fullmatch_any_tag(tag_pattern):
                yield connection

    def is_connected_with_tag(self, task_id: IdType, must_have_tag: str) -> bool:
        """Check if there is a connection to a task with given id that have the given tag."""
        cnct = self.find_connection(task_id)
        if cnct is None: return False
        return cnct.have_tag(must_have_tag)

    def is_connected_with_matching_tag(self, task_id: IdType, tag_pattern: str) -> bool:
        """Check if there is a connection to a task with given id that have at least one tag fully matching the given pattern."""
        cnct = self.find_connection(task_id)
        if cnct is None: return False
        return cnct.fullmatch_any_tag(tag_pattern)

    def union_connections(self, other) -> None:
        """Unite with other Connections."""
        self.data = Connections.__union_connections_sets(self.data, other.data)

    def add_connection(self, cnct: c.Connection) -> None:
        """Add a connection to connections."""
        self.__iadd__(cnct)

    def remove_connection(self, cnct: c.Connection) -> None:
        """Remove a connection from connections."""
        self.__delitem__(cnct)

    @classmethod
    def __union_connections_sets(cls, first: Set[c.Connection], second: Set[c.Connection]) -> Set[c.Connection]:
        """Unite 2 connections sets. If 2 connection objects have the same id's then unite their tags."""
        intersection: Set[c.Connection] = first & second
        result: Set[c.Connection] = first ^ second
        for connection in intersection:
            # Assume in each set can not appear 2 connections with the same id.
            current_id = connection.get_id()
            tags_from_first: Set[str] = next(cnct.tags for cnct in first if cnct.get_id() == current_id)
            tags_from_second: Set[str] = next(cnct.tags for cnct in second if cnct.get_id() == current_id)
            result.add(c.Connection(current_id, tags_from_first | tags_from_second))
        return result

    @classmethod
    def __check_iterable_have_only_connections(cls, value: Iterable) -> Iterable:
        """Raise an exception if not all elements of value are connection objects. Returns the passed Iterable."""
        # In case generator was passed, we can empty it. Copy the passed iterable and return it so it can be still available.
        value, value_copy = tee(value) 
        for cnt in value:
            if not isinstance(cnt, c.Connection):
                raise ValueError("Not all its elements are of type 'c.Connection'.")
        return value_copy

    def __getitem__(self, index: IdType) -> c.Connection:
        """Return connection object by task id."""
        return self.find_connection(index)

    def __iadd__(self, value):
        """Add connection objects. Argument can be either a Connections type, pure connection object or Iterable."""
        if isinstance(value, Connections):
            self.union_connections(value)
        elif isinstance(value, Iterable):
            self.union_connections(Connections(value))
        elif isinstance(value, c.Connection):
            self.union_connections(Connections([value, ]))
        elif isinstance(value, IdType):
            if value not in self.ids():
                self.data.add(c.Connection(value))
        else:
            raise TypeError(f"Unsupported operand type(s) for +=: 'Connections' and {type(value).__name__}")
        return self

    def __or__(self, other):
        """Union of 2 Connections."""
        return Connections(Connections.__union_connections_sets(self.data, other.data))

    def __ior__(self, other) -> None:
        """Perform union with other Connections."""
        self.__iadd__(other)

    def __iter__(self) -> Iterator:
        """Iterator over connection objects."""
        return self.data.__iter__()

    def __len__(self) -> int:
        """Return the count of connection objects inside this container."""
        return len(self.data)

    def __contains__(self, value) -> bool:
        """Check if value is contained in list. Argument can be a type of connection object or a task id."""
        if isinstance(value, IdType):
            id_to_find = value
            return self.find_connection(id_to_find) is not None
        connection_to_find: c.Connection = value
        return self.find_connection(connection_to_find.get_id()) == connection_to_find

    def __delitem__(self, key) -> None:
        """Delete connection object. Argument can be a type of connection object or a task id."""
        if self.__contains__(key):
            if isinstance(key, IdType):
                return self.data.discard(c.Connection(key))
            return self.data.discard(key)

    def __eq__(self, other) -> bool:
        """Compare 2 connetions object for equivalence."""
        if other is None: return False
        return json.dumps(self.to_json()) == json.dumps(other.to_json())

    def to_json(self) -> dict:
        """Return dictionary representation of the connections."""
        jsn: dict = dict()
        for cnt in sorted(list(self.data)):
            jsn[cnt.get_id()] = list(sorted(list(cnt.tags)))
        return jsn

    def __repr__(self) -> str:
        """Return string representation of the connections container."""
        return f"<Connections {self.data}>"
