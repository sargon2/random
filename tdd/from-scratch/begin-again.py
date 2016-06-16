#!/usr/bin/env python

def assert_true(item):
    with should_fail():
        assert_false(item)

def fail():
    with should_fail():
        pass

def assert_false(item):
    if item:
        fail()

class should_fail():
    def __enter__(self):
        pass

    def __exit__(self, type, msg, tb):
        if type is AssertionError:
            return True
        # This raise is untested because it's impossible to test it without duplication.
        # That means it's really configuration -- we're configuring what to do when a test fails.
        raise AssertionError("Expected a failure")

def assert_equals(a, b):
    assert_true(a == b)

def assert_not_equals(a, b):
    with should_fail():
        assert_equals(a, b)

assert_true(True)
assert_false(False)

with should_fail():
    assert_true(False)

with should_fail():
    assert_false(True)

with should_fail():
    fail()

assert_equals(1, 1)
with should_fail():
    assert_equals(1, 2)

assert_not_equals(1, 2)
with should_fail():
    assert_not_equals(1, 1)

print "pass"
