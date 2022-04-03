"""Tests for connections class."""

import unittest
from tasktree.core.connection import Connection
from tasktree.core.connections import Connections

# Disable invalid names & missing docstrings:
# pylint: disable=C0116,C0103
class TestConnections(unittest.TestCase):
    """Class for checking operations on several connections."""

    default_id = "123456"
    other_id = "654321"
    new_id = "1010101010"

    def test_init_wrong_iterable_raise_exception(self):
        with self.assertRaises(Exception):
            Connections([Connection(self.default_id), 2])
        with self.assertRaises(Exception):
            Connections([3, Connection(self.default_id)])
        with self.assertRaises(Exception):
            Connections([3, 15])

    def test_init_with_normal_iterable_sets_correct_iterator(self):
        cnct_set: set = {Connection(self.default_id), 
                         Connection(self.other_id), 
                         Connection(self.other_id)}
        cncts = Connections(cnct_set)
        self.assertSequenceEqual(cncts.data, cnct_set)

    def test_init_with_autoconnect_to_self_is_correct_by_calling_find_connection_func(self):
        cncts = Connections({Connection(self.default_id)}, self_id=self.other_id)
        self.assertIn(Connection(self.default_id), cncts)
        self.assertIn(Connection(self.other_id), cncts)
        self.assertTrue(cncts.find_connection(self.other_id).is_self())
        self.assertTrue(cncts.find_connection(self.other_id).have_tag("guard"))

    def test_find_connection_on_empty_container_return_none(self):
        cncts = Connections()
        self.assertIsNone(cncts.find_connection(self.default_id))

    def test_find_connection(self):
        cnct_set: set = {Connection(self.default_id), 
                         Connection(self.other_id), 
                         Connection(self.new_id)}
        cncts = Connections(cnct_set)
        self.assertIsNotNone(cncts.find_connection(self.default_id))
        self.assertIsNotNone(cncts.find_connection(self.other_id))
        self.assertIsNotNone(cncts.find_connection(self.new_id))
        self.assertIsNone(cncts.find_connection(""))

    def test_ids_generator_works_correctly_also_check_length(self):
        ids_set: set = {self.default_id, self.other_id, self.new_id}
        cncts = Connections(Connection(id) for id in ids_set)
        self.assertSequenceEqual(ids_set, set(cncts.ids()))
        self.assertEqual(len(ids_set), len(cncts))

    def test_ids_generator_works_correctly_empty_initialization_also_check_length(self):
        cncts = Connections()
        self.assertSequenceEqual(set(), set(cncts.ids()))
        self.assertEqual( 0, len(cncts) )

    def test_with_tag_works_correctly_on_several_connections(self):
        cnct_set: set = {Connection(self.default_id, ["self", "other"]), 
                         Connection(self.other_id, ["yes"]), 
                        }
        cncts = Connections(cnct_set, self_id=self.new_id )

        supposed_result_for_self = {Connection(self.default_id), Connection(self.new_id)}
        self.assertSequenceEqual(supposed_result_for_self, set(cncts.with_tag("self")))

        supposed_result_for_other = {Connection(self.default_id)}
        self.assertSequenceEqual(supposed_result_for_other, set(cncts.with_tag("other")))

        self.assertSequenceEqual(set(), set(cncts.with_tag("no_such_tag_belive_me")))

    def test_iteration_over_object(self):
        cnct_set: set = {Connection(self.default_id, ["self", "other"]), 
                         Connection(self.other_id, ["yes"])
                        }
        cncts = Connections(cnct_set, self_id=self.new_id )
        cnct_set.add(Connection(self.new_id))
        self.assertSequenceEqual(list(cnct_set), list(cncts))

    def test_with_tag_empty_on_empty_initialization(self):
        cncts = Connections()
        self.assertSequenceEqual(set(), set(cncts.with_tag("no_such_tag_belive_me")))

    def test_match_tag_works_correctly_on_several_connections_and_getitem_tests(self):
        cnct_dict: dict = {self.default_id: Connection(self.default_id, ["abcd", "abcdd"]), 
                         self.other_id: Connection(self.other_id, ["012d"]), 
                         self.new_id: Connection(self.new_id, ["0123"])
                        }
        cncts = Connections(cnct_dict.values())

        for test_case in [({self.default_id, self.other_id}, ".*d+"),
                          ({self.other_id, self.new_id}, "012."),
                          ({self.new_id}, "[0-9]+")]:
            supposed_result = {Connection(id) for id in test_case[0]}
            self.assertSequenceEqual(supposed_result, set(cncts.match_tag(test_case[1])))
            # Check also that tags are correct (__getitem__ function):
            for id in test_case[0]:
                self.assertEqual(cnct_dict[id], cncts[id])

    def test_is_connected_with_tag(self):
        cnct_set: set = {Connection(self.default_id, ["self", "other"]), 
                         Connection(self.other_id, ["yes"])
                        }
        cncts = Connections(cnct_set)
        self.assertFalse(cncts.is_connected_with_tag(self.other_id, "no_such_tag_belive_me"))
        self.assertFalse(cncts.is_connected_with_tag(self.new_id, "self"))
        for c in cnct_set:
            for t in c.tags:
                self.assertTrue(cncts.is_connected_with_tag(c.get_id(), t))

    def test_is_connected_with_matching_tag(self):
        cnct_set: set = {Connection(self.default_id, ["self", "other"]), 
                         Connection(self.other_id, ["yes"])
                        }
        cncts = Connections(cnct_set)
        self.assertFalse(cncts.is_connected_with_matching_tag(self.other_id, "ye?"))
        self.assertFalse(cncts.is_connected_with_matching_tag(self.new_id, ".*"))
        self.assertTrue(cncts.is_connected_with_matching_tag(self.other_id, ".*"))
        self.assertTrue(cncts.is_connected_with_matching_tag(self.other_id, "yesd?"))
        self.assertTrue(cncts.is_connected_with_matching_tag(self.default_id, "[so].*e.*"))
        self.assertTrue(cncts.is_connected_with_matching_tag(self.default_id, "self$"))

    def test_is_connected_with_matching_tag(self):
        first = Connections({Connection(self.default_id, ["self", "other"]), 
                             Connection(self.other_id, ["yes"])
                            })
        second = Connections({Connection(self.new_id, ["no", "whatever"]), 
                             Connection(self.other_id, ["yes", "something_new"])
                            })
        result = Connections({Connection(self.default_id, ["self", "other"]),
                             Connection(self.new_id, ["no", "whatever"]), 
                             Connection(self.other_id, ["yes", "something_new"])
                            })
        self.assertEqual( (first | second), result)
