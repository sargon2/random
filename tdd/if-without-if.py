
import unittest2

# Testing the "replace conditional with polymorphism" refactoring.

class TestBefore(unittest2.TestCase):

    def before(self, arg):
        if arg:
            return 1
        else:
            return "a"

    def test_before(self):
        self.assertEquals(1, self.before(True))
        self.assertEquals("a", self.before(False))

# The goal is to replace the if with polymorphism.  The final state should have no if statements at all.

class TrueThing(object):
    def get(self):
        return 1

class FalseThing(object):
    def get(self):
        return "a"

class TestAfter(unittest2.TestCase):

    def after(self, arg):
        return arg.get()

    def test_after(self):
        self.assertEquals(1, self.after(TrueThing()))
        self.assertEquals("a", self.after(FalseThing()))

# There's an implicit if there, in choosing which class to instantiate.  The argument is that one if there is better than many downstream.
