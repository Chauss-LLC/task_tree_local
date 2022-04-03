"""Tests for connection class."""

import unittest
from tasktree.core.connection import Connection

# Disable invalid names & missing docstrings:
# pylint: disable=C0116,C0103
class TestConnection(unittest.TestCase):
    """Class for checking connection operations."""

    default_id = "123456"
    other_id = "654321"

    def test_connection_creation_raises_ValueError_if_id_is_empty_string(self):
        # TODOwith self.assertRaises(Exception):
            Connection("")

    def test_new_connection_have_correct_id(self):
        CONNECTION_ID: str = TestConnection.default_id
        cnct = Connection(CONNECTION_ID)
        self.assertEqual(cnct.get_id(), CONNECTION_ID)

    def test_new_connection_dont_have_tags(self):
        cnct = Connection(TestConnection.default_id)
        self.assertSequenceEqual(cnct.tags, [])

    def test_new_empty_connection_is_not_self(self):
        cnct = Connection(TestConnection.default_id)
        self.assertFalse(cnct.is_self())

    def test_new_empty_connection_is_not_child(self):
        cnct = Connection(TestConnection.default_id)
        self.assertFalse(cnct.is_child())

    def test_new_empty_connection_is_not_parent(self):
        cnct = Connection(TestConnection.default_id)
        self.assertFalse(cnct.is_parent())

    def test_connection_have_added_tag(self):
        test_tag: str = 'any'
        cnct = Connection(TestConnection.default_id)
        cnct.add_tag(test_tag)
        self.assertTrue(cnct.have_tag(test_tag))

    def test_connection_with_passed_tags_is_self(self):
        cnct = Connection(TestConnection.default_id, [Connection.CHILD_TAG, 
                                                      Connection.SELF_TAG, 
                                                      Connection.PARENT_TAG])
        self.assertTrue(cnct.is_self())

    def test_connection_with_passed_tags_is_child(self):
        cnct = Connection(TestConnection.default_id, [Connection.CHILD_TAG, 
                                                      Connection.SELF_TAG, 
                                                      Connection.PARENT_TAG])
        self.assertTrue(cnct.is_child())

    def test_connection_with_passed_tags_is_parent(self):
        cnct = Connection(TestConnection.default_id, [Connection.CHILD_TAG, 
                                                      Connection.SELF_TAG, 
                                                      Connection.PARENT_TAG])
        self.assertTrue(cnct.is_parent())

    def test_connection_after_adding_and_removing_tags_sequence_have_no_tags(self):
        cnct = Connection(TestConnection.default_id)
        test_tags: list = ['any', 'test1', 'test2']
        for tag in test_tags:
            cnct.add_tag(tag)
        for tag in test_tags:
            cnct.remove_tag(tag)
        self.assertSequenceEqual(cnct.tags, [])

    def test_adding_the_same_tag_return_false(self):
        cnct = Connection(TestConnection.default_id)
        test_tag: str = 'any'
        cnct.add_tag(test_tag)
        self.assertFalse(cnct.add_tag(test_tag))

    def test_removing_tag_from_empty_connection_return_false(self):
        cnct = Connection(TestConnection.default_id)
        test_tag: str = 'any'
        self.assertFalse(cnct.remove_tag(test_tag))

    def test_connection_do_not_have_tag_after_remove(self):
        test_tag: str = 'any'
        cnct = Connection(TestConnection.default_id, [test_tag,])
        cnct.remove_tag(test_tag)
        self.assertFalse(cnct.have_tag(test_tag))

    def test_connections_are_same_after_create_with_same_id(self):
        cnct = Connection(TestConnection.default_id)
        cnct2 = Connection(TestConnection.default_id)
        self.assertTrue(cnct == cnct2)
        self.assertFalse(cnct != cnct2)

    def test_connections_are_same_even_when_different_tags(self):
        cnct = Connection(TestConnection.default_id, ['any', 'any2'])
        cnct2 = Connection(TestConnection.default_id, ['other'])
        self.assertTrue(cnct == cnct2)
        self.assertFalse(cnct != cnct2)

    def test_connections_not_same_when_create_with_different_id(self):
        cnct = Connection(TestConnection.default_id)
        cnct2 = Connection(TestConnection.other_id)
        self.assertTrue(cnct != cnct2)
        self.assertFalse(cnct == cnct2)

    def test_connections_set_do_not_changes_when_add_connection_with_same_id(self):
        s: set = {Connection(TestConnection.default_id)}
        b = set(s)
        s.add(Connection(TestConnection.default_id))
        self.assertTrue(s == b)

    def test_connection_can_not_change_id(self):
        cnct = Connection(TestConnection.default_id)
        with self.assertRaises(Exception):
            cnct._id = TestConnection.other_id

    def test_connection_after_copy_have_correct_tags(self):
        test_tags: set = {'any', 'other', 'other2'}
        cnct = Connection(TestConnection.default_id, test_tags)
        cnct2 = cnct.copy(TestConnection.other_id)
        self.assertSequenceEqual(test_tags, cnct2.tags)

    def test_connection_copy_with_same_id_raises_exception(self):
        cnct = Connection(TestConnection.default_id)
        with self.assertRaises(Exception):
            cnct2 = cnct.copy(TestConnection.default_id)

    def test_fullmatch_any_tag_works_correct_on_nonempty_tags_sest(self):
        test_tags: set = {'any', 'other', 'other2'}
        cnct = Connection(TestConnection.default_id, test_tags)
        self.assertTrue(cnct.fullmatch_any_tag("o\w*r")) # one match.
        self.assertTrue(cnct.fullmatch_any_tag("^[a-zA-Z]+$")) # all matches.
        self.assertTrue(cnct.fullmatch_any_tag("other2?")) # 2 matches.
        self.assertFalse(cnct.fullmatch_any_tag("oth+")) # 0 matches.

    def test_fullmatch_any_tag_works_correct_on_empty_tags_sest(self):
        cnct = Connection(TestConnection.default_id)
        self.assertFalse(cnct.fullmatch_any_tag("o\w*r"))
        self.assertFalse(cnct.fullmatch_any_tag(""))
