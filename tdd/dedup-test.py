# Removing complexity between test code and real code.
# I tried to dedup the if a == b that assertEquals uses.

import unittest2

def ifeq(a, b, r1, r2):
    if a == b:
        return r1
    return r2

def realfunc(a, b):
    return ifeq(a, b, "1", "2")

def tf(a, b):
    return ifeq(a, b, True, False)

def tfr(a, b, c):
    return tf(realfunc(a, b), c)

class thing(unittest2.TestCase):
    def test_a(self):
        self.assertTrue(tfr("a", "a", "1"))
        self.assertTrue(tfr("a", "b", "2"))

    def test_b(self):
        self.assertFalse(tfr("a", "a", "2"))
        self.assertFalse(tfr("a", "b", "1"))

# Thoughts:
# The code that is deduped between test code and real code is real code.
# Test code should not have if statements in it because if it does, the if should be refactored out into product code.
# If the program processes data, the test inputs should be data.
# Wrapping complexity in a function counts as deduplicating the complexity.  A function that consists only of function calls is complexity 0.
