import unittest2
import statefulboolean
import os

# Problem.  How do we TDD something with permanant state?
# When we start the test run, it has a state.  We don't know what that state is.

# We have operations get_state() and set_state().

# Since the test starts with new state each time, it has no way to verify that the state is stored across reboots.

# Option: mock the thing that stores the state permanantly, don't test it.

# Option: put code to read the permanant state in the test.  Then invoke the real code to write it and assert it changed.
#   - But that should be dedup'd with the live code that reads the state.  And at that point it could be changed to be non-permanant.

# Option: Python has a reload() function.  It only works on modules.

# TODO: nose2 parameterized tests


def collect(appendable):
    def level2(method):
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        appendable.append(wrapper)
        return wrapper
    return level2

state_methods = []
class TestSomething(unittest2.TestCase):

    @collect(state_methods)
    def assert_set_get_state_single(self, state):
        sb = statefulboolean.StatefulBoolean()
        sb.set_state(state)
        self.assertEquals(state, sb.get_state())

    @collect(state_methods)
    def assert_set_get_state(self, state):
        sb1 = statefulboolean.StatefulBoolean()
        sb1.set_state(state)
        sb1 = None

        sb2 = statefulboolean.StatefulBoolean()
        self.assertEquals(state, sb2.get_state())

    @collect(state_methods)
    def assert_already_exists_get(self, state):
        sb1 = statefulboolean.StatefulBoolean()
        sb2 = statefulboolean.StatefulBoolean()

        sb1.set_state(state)
        self.assertEquals(state, sb2.get_state())

    def assert_state_changer(self, state, method):
        sb1 = statefulboolean.StatefulBoolean()
        sb1.set_state(state)

        method()

        sb2 = statefulboolean.StatefulBoolean()
        self.assertEquals(state, sb2.get_state())

    @collect(state_methods)
    def assert_state_changers(self, state):
        changers = []

        @collect(changers)
        def rel():
            reload(statefulboolean)

        @collect(changers)
        def chdir():
            os.chdir("/")

        for changer in changers:
            self.assert_state_changer(state, changer)

    def try_all(self, state):
        for method in state_methods:
            method(self, state)

    def test_set_get(self):
        data = [True, False, "a"]
        for item in data:
            self.try_all(item)


