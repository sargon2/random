#!/usr/bin/env python

from contextlib import contextmanager
import traceback

class TestFramework(object):
    @contextmanager
    def assert_fails(self):
        try:
            yield
        except AssertionError:
            pass
        else:
            self.fail("test should have failed but didn't")

    def fail(self, msg=""):
        raise AssertionError(msg)

    def assert_equals(self, a, b):
        if a != b:
            self.fail(str(a) + " != " + str(b))

tests = []
def Test(a):
    tests.append(a)
    return a

class TestTestFramework(TestFramework):

    def failing_test(self):
        self.fail()

    @Test
    def test_test_can_fail(self):
        with self.assert_fails():
            self.failing_test()

    @Test
    def test_assert_equals_pass(self):
        self.assert_equals(True, True)
        self.assert_equals(1, 1)

    @Test
    def test_assert_equals_fail(self):
        with self.assert_fails():
            self.assert_equals(True, False)


t = TestTestFramework()
num_tests = 0
num_failures = 0
for test in tests:
    try:
        num_tests += 1
        test(t)
    except:
        num_failures += 1
        traceback.print_exc()
        print
print str(num_tests) + " tests ran, " + str(num_failures) + " failed"
