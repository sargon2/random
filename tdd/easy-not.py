import unittest2

class Negativizer(object): # TODO: name
    def __init__(self, parent):
        self.parent = parent

    def __getattr__(self, name):
        def replacement_method(*args, **kwargs):
            try:
                self.parent.__getattribute__(name)(*args, **kwargs)
            except AssertionError:
                pass
            else:
                raise AssertionError # TODO: message
        return replacement_method


class BaseEasyNot(unittest2.TestCase):
    def setUp(self):
        self.Not = Negativizer(self)


class TestEasyNot(BaseEasyNot):
    def test_passes(self):
        self.assertEquals(1, 1)
        self.Not.assertEquals(1, 2)

    def test_equals_fails(self):
        with self.assertRaises(AssertionError):
            self.assertEquals(1, 2)

    def test_not_equals_fails(self):
        with self.assertRaises(AssertionError):
            self.Not.assertEquals(1, 1)
