# My try1 code had a weird smell with @collect.  So I wanted to go through the process again to see if I could do better the 2nd time.

import unittest2
import storage
import sys
import re
import os

# TODO: deletion

class TestStoreState(unittest2.TestCase):
    def reload_python_state(self):
        # Our module under test might delegate the in-memory storage to another module.
        # So, we reload as much as we can in sys.modules.
        for module_name, value in sys.modules.iteritems():
            reload_ok = True

            # Some things don't deal well with being reload()ed.  So we don't reload those things.
            if value is None:
                reload_ok = False

            do_not_reload_regexes = [
                    r'^six',
                    r'^unittest',
                    r'^zipfile$',
                    r'^__main__$',
                    r'^site$',
                    r'^nose'
                ]
            for regex in do_not_reload_regexes:
                if re.match(regex, module_name):
                    reload_ok = False

            if reload_ok:
                reload(value)

        # The app could have stored its state in cwd, so to avoid that let's change cwd.
        os.chdir("/")

    # We have to be able to store and get things from memory to test that our reload_python_state method works.
    def assert_store_get_memory(self, value):
        storage.store_in_memory(value)
        self.assertEquals(value, storage.get_from_memory())

    def test_store_get_memory(self):
        # Just try two different values to make sure it's not hardcoded
        self.assert_store_get_memory(True)
        self.assert_store_get_memory(False)

    def test_in_memory_item_default_value(self):
        self.assertEquals(None, storage.get_from_memory())

    def test_reload_state_reloads(self):
        storage.store_in_memory(True)
        self.reload_python_state()
        self.assertEquals(None, storage.get_from_memory())

    # Now, we finally get to the fun persistence test.
    def assert_store_get_persistent(self, value):
        storage.store("key", value)
        self.reload_python_state()
        self.assertEquals(value, storage.get("key"))

    def test_store_get_persistent(self):
        self.assert_store_get_persistent("a")
        self.assert_store_get_persistent([1, 2, 3])
        self.assert_store_get_persistent({'a': 3, 'b': 5})

    def test_what(self):
        storage.store("key", "a")
        storage.store("key2", "b")
        self.assertEquals("a", storage.get("key"))
        self.assertEquals("b", storage.get("key2"))
