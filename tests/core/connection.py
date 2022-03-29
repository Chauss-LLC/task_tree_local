"""Tests for connection class."""

import unittest
from tasktree.core.connection import Connection


# pylint: disable=C0116,C0103
class TestConnection(unittest.TestCase):
    """Class for checking connection operations."""

    default_id = "123456"

    def test_connection_creation_raises_ValueError_if_id_is_empty_string(self):
        def create_connection_empty_id():
            Connection("", [])

        self.assertRaises(ValueError, create_connection_empty_id)

    def test_new_connection_have_correct_id(self):
        CONNECTION_ID: str = TestConnection.default_id
        c = Connection(CONNECTION_ID, [])
        self.assertEqual(c.id, CONNECTION_ID)

    def test_new_connection_dont_have_tags(self):
        c = Connection(TestConnection.default_id, [])
        self.assertSequenceEqual(c.tags, [])

    def test_new_empty_connection_is_not_self(self):
        c = Connection(TestConnection.default_id, [])
        self.assertFalse(c.is_self())
