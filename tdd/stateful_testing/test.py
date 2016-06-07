# My try1 code had a weird smell with @collect.  So I wanted to go through the process again to see if I could do better the 2nd time.

import unittest2
import storage
import types

# TODO: the module is storing in cwd so try a chdir
# TODO: store 2 values, get both back

class TestStoreState(unittest2.TestCase):
    # There's a list of all modules in sys.modules.  I tried reloading all those, and it actually reloaded the unittest2/nosetest state, aborting the test run!
    # So, we just reload things in the global state in this class.
    def reload_python_state(self):
        for name, val in globals().items():
            if isinstance(val, types.ModuleType):
                reload(val)

    # We have to be able to store and get things from memory to test that our reload_python_state method works.
    def assert_store_get_memory(self, value):
        storage.store_in_memory(value)
        self.assertEquals(value, storage.get_from_memory())

    def test_store_get_memory(self):
        self.assert_store_get_memory(True)
        self.assert_store_get_memory(False)
        self.assert_store_get_memory("a")

    def test_in_memory_item_default_value(self):
        self.assertEquals(None, storage.get_from_memory())

    def test_reload_state_reloads(self):
        storage.store_in_memory(True)
        self.reload_python_state()
        self.assertEquals(None, storage.get_from_memory())

    # Now, we finally get to the fun persistence test.
    def assert_store_get_persistent(self, value):
        storage.store(value)
        self.reload_python_state()
        self.assertEquals(value, storage.get())

    def test_store_get_persistent(self): # TODO: looks dup'd with test_store_get_memory
        self.assert_store_get_persistent(True)
        self.assert_store_get_persistent(False)
        self.assert_store_get_persistent("a")
