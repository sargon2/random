
import unittest

# For this attempt, I decided to write an object to represent part of an array.
# It seemed very condusive to recursion, so I also tried it with recursion.
# I think adding in the recursion made it harder, and adding in the object made it easier.

class ArrayPart(object):

    def __init__(self, array, start=None, end=None, offset=0):
        self.offset = offset
        if array is None:
            raise Exception("invalid argument None for array")
        if start is None:
            self.array = array
        else:
            if end is None:
                self.array = array[start:]
            else:
                self.array = array[start:end+1] # should this have been just start:end?

    def get_array(self):
        return self.array

    def get_midpoint(self):
        return len(self.array)/2

    def get_left_half(self):
        return ArrayPart(self.array, 0, self.get_midpoint()-1, offset=self.offset)

    def get_right_half(self):
        midpoint = self.get_midpoint()
        return ArrayPart(self.array, midpoint, offset=self.offset + midpoint)

    def binary_search(self, needle):
        if len(self.array) == 0:
            return None
        midpoint = self.get_midpoint()
        val = self.array[midpoint]
        if val < needle: # the midpoint is less than the needle, so go right
            if len(self.array) == 1: # why do I need this?
                return None
            return self.get_right_half().binary_search(needle)
        if val > needle:
            return self.get_left_half().binary_search(needle)
        # Equal
        return midpoint + self.offset


class TestArrayPart(unittest.TestCase):

    def assert_get_array(self, expected, input_array, input_start, input_end):
        self.assertEquals(expected, ArrayPart(input_array, input_start, input_end).get_array())

    def assert_get_left(self, expected, input_array):
        self.assertEquals(expected, ArrayPart(input_array).get_left_half().get_array())

    def assert_get_right(self, expected, input_array):
        self.assertEquals(expected, ArrayPart(input_array).get_right_half().get_array())

    def test_init_no_slicing(self):
        a = ArrayPart([1])
        self.assertEquals([1], a.get_array())

    def test_init_none(self):
        try:
            ArrayPart(None)
        except:
            pass
        else:
            self.fail("expected an exception")

    def test_init_empty(self):
        a = ArrayPart([])
        self.assertEquals([], a.get_array())
        self.assertEquals([], a.get_left_half().get_array())
        self.assertEquals([], a.get_right_half().get_array())

    def test_whole_array(self):
        self.assert_get_array([1], [1], 0, 0)
        self.assert_get_array([1, 2], [1, 2], 0, 1)
        self.assert_get_array([2, 3], [2, 3], 0, 1)
        self.assert_get_array([1, 2, 3], [1, 2, 3], 0, 2)

    def test_subset(self):
        self.assert_get_array([1], [1, 2, 3], 0, 0)
        self.assert_get_array([2], [1, 2, 3], 1, 1)
        self.assert_get_array([1, 2], [1, 2, 3], 0, 1)
        self.assert_get_array([2, 3], [1, 2, 3], 1, 2)

    def test_get_left_half_even(self):
        self.assert_get_left([1], [1, 2])
        self.assert_get_left([2], [2, 3])
        self.assert_get_left([1, 2], [1, 2, 3, 4])

    def test_get_right_half_even(self):
        self.assert_get_right([2], [1, 2])
        self.assert_get_right([3], [2, 3])
        self.assert_get_right([3, 4], [1, 2, 3, 4])

    def test_get_left_half_odd(self):
        self.assert_get_left([], [1])
        self.assert_get_left([], [2])
        self.assert_get_left([1], [1, 2, 3])
        self.assert_get_left([1, 2], [1, 2, 3, 4, 5])

    def test_get_right_half_odd(self):
        self.assert_get_right([1], [1])
        self.assert_get_right([2], [2])
        self.assert_get_right([2, 3], [1, 2, 3])
        self.assert_get_right([3, 4, 5], [1, 2, 3, 4, 5])


class TestBinarySearch(unittest.TestCase):
    def binary_search(self, needle, haystack):
        if len(haystack) == 0:
            return None
        a = ArrayPart(haystack)
        return a.binary_search(needle)
    def test_binary_search(self):
        # Shamelessly copied from kata 2-1
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
