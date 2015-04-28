# https://leetcode.com/problems/single-number/

import unittest2

def single_number(nums):
    return single_number_set(nums)

def single_number_set(nums):
    # Sets in python are O(1) for insert, remove, and pop.
    # But this still feels like cheating.
    numset = set()
    for num in nums:
        if num in numset:
            numset.remove(num)
        else:
            numset.add(num)
    return numset.pop()

class TestSingleNumber(unittest2.TestCase):
    def test_something(self):
        self.assertEquals(3, single_number([1, 1, 2, 2, 3]))
        self.assertEquals(3, single_number([1, 1, 3, 2, 2]))
        self.assertEquals(3, single_number([1, 2, 3, 1, 2]))
        self.assertEquals(4, single_number([1, 2, 3, 3, 1, 2, 4]))
        self.assertEquals(4, single_number([1, 2, 3, 3, 1, 4, 2]))
