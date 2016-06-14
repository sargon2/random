#!/usr/bin/env python

# In the kata fashion let's try this from scratch again.

# Start from should_fail.  That's an interesting one because it's hard to automatically test it.  If you write a test for it, the test should be deduped with it!

from contextlib import contextmanager

# UNTESTED:
@contextmanager
def should_fail():
    try:
        yield
    except AssertionError:
        pass
    else:
        raise AssertionError("Expected an AssertionError")
# END UNTESTED

def fail():
    raise AssertionError("fail")

def test1():
    with should_fail():
        fail()

def assert_true(item):
    with should_fail():
        assert_false(item)

def assert_false(item):
    if item:
        raise AssertionError(str(item) + " was True, should have been False")

def test_assert_true():
    assert_true(True)
    with should_fail():
        assert_true(False)

def test_assert_false():
    assert_false(False)
    with should_fail():
        assert_false(True)

test1()
test_assert_true()
test_assert_false()
