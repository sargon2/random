#!/usr/bin/env python

def assert_true(item):
    with should_fail():
        assert_false(item)

def assert_false(item):
    if item:
        raise AssertionError(str(item) + " was True, expected False")

class should_fail():
    def __enter__(self):
        pass

    def __exit__(self, type, msg, tb):
        if type is AssertionError:
            return True
        # This raise is untested because it's impossible to test it without duplication.
        raise AssertionError("Expected a failure")

def assert_equals(a, b):
    with should_fail():
        assert_not_equals(a, b)

def assert_not_equals(a, b):
    if a == b:
        raise AssertionError(str(a) + " == " + str(b))

assert_true(True)
assert_false(False)

with should_fail():
    assert_true(False)

with should_fail():
    assert_false(True)

with should_fail():
    with should_fail():
        pass

assert_equals(1, 1)
with should_fail():
    assert_equals(1, 2)

assert_not_equals(1, 2)
with should_fail():
    assert_not_equals(1, 1)
