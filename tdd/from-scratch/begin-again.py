#!/usr/bin/env python

def assert_true(item, msg=None):
    if not msg:
        msg = "Expected " + str(item) + " to be True"
    with should_fail(msg):
        assert_false(item)

def fail(msg="failed"):
    with should_fail(msg):
        pass

def assert_false(item):
    if item:
        fail("Expected " + str(item) + " to be False")

class should_fail(object):
    def __init__(self, msg="Expected a failure", expected_msg=None):
        self.msg = msg
        self.expected_msg = expected_msg

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc, tb):
        if exc_type is AssertionError:
            if not self.expected_msg or str(exc) == self.expected_msg:
                return True
            raise AssertionError("Expected exception message '" + str(exc) + "' to be '" + str(self.expected_msg) + "'")
        # This raise is untested because it's impossible to test it without duplication.
        # That means it's really configuration -- we're configuring what to do when a test fails.
        raise AssertionError(self.msg)

def assert_equals(a, b):
    assert_true(a == b, "Expected " + str(a) + " to equal " + str(b))

def assert_not_equals(a, b):
    with should_fail(msg="Expected " + str(a) + " to not equal " + str(b)):
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

with should_fail(expected_msg="Expected exception message 'jkl' to be 'asdf'"):
    with should_fail(expected_msg="asdf"):
        fail("jkl")

with should_fail(expected_msg="asdf"):
    fail("asdf")

with should_fail(expected_msg="Expected False to be True"):
    assert_true(False)

with should_fail(expected_msg="Expected True to be False"):
    assert_false(True)

with should_fail(expected_msg="Expected 1 to equal 2"):
    assert_equals(1, 2)

with should_fail(expected_msg="Expected 1 to not equal 1"):
    assert_not_equals(1, 1)

print "pass"
