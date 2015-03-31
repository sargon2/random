import unittest2

class TestSomething(unittest2.TestCase):
    def test_something(self):
        # The idea here is if method is defined the same, method(list) should iterate and method(arg) should run once.
        # But then what about 2-arg methods?  method(list, list) should run list*list times.
        self.fail("Not written yet")
