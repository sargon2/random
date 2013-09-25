
import unittest

# Implementation 1 of kata 2.
# For this implementation, I will do it basically non-TDD; just write the algorithm.

# After implementing:
# I might have too many if statements.
# The +1 on low = midpoint + 1 was difficult.
# The off-by-one on high was expected, but still harder than it should have been to add.

class Test(unittest.TestCase):

    def binary_search(self, needle, haystack):
        if len(haystack) == 0:
            return None
        low = 0
        high = len(haystack) - 1
        while low != high:
            midpoint = (low+high)/2
            value = haystack[midpoint]
            if value == needle:
                return midpoint
            if value <= needle:
                low = midpoint + 1
            if value > needle:
                high = midpoint
        if haystack[low] != needle:
            return None
        return low

    def test_binary_search(self):
        self.assertEqual(None, self.binary_search(1, []))
        self.assertEqual(0, self.binary_search(1, [1]))
        self.assertEqual(0, self.binary_search(1, [1, 2]))
        self.assertEqual(1, self.binary_search(2, [1, 2]))
        self.assertEqual(None, self.binary_search(1, [2]))

        self.assertEqual(0,  self.binary_search(1, [1, 3, 5]))
        self.assertEqual(1,  self.binary_search(3, [1, 3, 5]))
        self.assertEqual(2,  self.binary_search(5, [1, 3, 5]))
        self.assertEqual(None, self.binary_search(0, [1, 3, 5]))
        self.assertEqual(None, self.binary_search(2, [1, 3, 5]))
        self.assertEqual(None, self.binary_search(4, [1, 3, 5]))
        self.assertEqual(None, self.binary_search(6, [1, 3, 5]))

        self.assertEqual(0,  self.binary_search(1, [1, 3, 5, 7]))
        self.assertEqual(1,  self.binary_search(3, [1, 3, 5, 7]))
        self.assertEqual(2,  self.binary_search(5, [1, 3, 5, 7]))
        self.assertEqual(3,  self.binary_search(7, [1, 3, 5, 7]))
        self.assertEqual(None, self.binary_search(0, [1, 3, 5, 7]))
        self.assertEqual(None, self.binary_search(2, [1, 3, 5, 7]))
        self.assertEqual(None, self.binary_search(4, [1, 3, 5, 7]))
        self.assertEqual(None, self.binary_search(6, [1, 3, 5, 7]))
        self.assertEqual(None, self.binary_search(8, [1, 3, 5, 7]))
