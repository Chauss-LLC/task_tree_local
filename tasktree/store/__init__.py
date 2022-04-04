"""
Packege for saving and loading data.

Different places for store supported.
"""
# from tasktree.store.json_store import JsonStore
from tasktree.store.pickle_store import PickleStore


store = PickleStore("/tmp/tt_stored.pickle")  # TODO: chose another directory
