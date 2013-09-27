
import unittest
import operator

# For this attempt, I want to write a binary search that operates on arbitrary-length streams of data.

# (after writing) This is really slick.  I love it.  It is really incredible that we can find the upper/lower bounds within O(logn).

# We could write a generator that returns values from an array, and -inf/+inf for values outside the range of the array.
# (or just call real_binary_search with the array bounds :/)

class LinearGenerator(object):
    def get_value_at(self, index):
        return index * 2

class TestLinearGenerator(unittest.TestCase):
    def test_get_value_at(self):
        l = LinearGenerator()
        self.assertEquals(2, l.get_value_at(1))
        self.assertEquals(2000, l.get_value_at(1000))

class TestBinarySearch(unittest.TestCase):

    def real_binary_search(self, key, generator, left, right):
        midpoint = (left + right) / 2
        midpoint_value = generator.get_value_at(midpoint)
        if midpoint_value == key:
            return midpoint
        if left == right:
            return None
        if midpoint_value > key:
            return self.real_binary_search(key, generator, left, midpoint)
        else:
            return self.real_binary_search(key, generator, midpoint+1, right)

    def _double_until(self, key, generator, init):
        if init > 0:
            op = operator.lt
        else:
            op = operator.gt
        max = init
        while op(generator.get_value_at(max),key):
            max *= 2
        return max

    def find_right(self, key, generator):
        return self._double_until(key, generator, 1)

    def find_left(self, key, generator):
        return self._double_until(key, generator, -1)

    def binary_search(self, key, generator):
        if key is None:
            return None
        right = self.find_right(key, generator)
        left = self.find_left(key, generator)
        return self.real_binary_search(key, generator, left, right)

    def test_binary_search(self):
        self.assertEquals(None, self.binary_search(None, LinearGenerator()))
        self.assertEquals(0, self.binary_search(0, LinearGenerator()))
        self.assertEquals(1, self.binary_search(2, LinearGenerator()))
        self.assertEquals(2, self.binary_search(4, LinearGenerator()))
        self.assertEquals(3, self.binary_search(6, LinearGenerator()))
        self.assertEquals(None, self.binary_search(1, LinearGenerator()))
        self.assertEquals(None, self.binary_search(3, LinearGenerator()))
        self.assertEquals(None, self.binary_search(1.5, LinearGenerator()))

        # Just to make sure there's no cheating...
        self.assertEquals(3000000000, self.binary_search(6000000000, LinearGenerator()))

        self.assertEquals(-1, self.binary_search(-2, LinearGenerator()))
