import unittest2

# O(n) integer sort if the largest element in the array is O(n) and the smallest is >= 0.

# This is technically O(n) but for some reason the builtin sort is outperforming it.

def count_sort(in_ary):
    return my_count_sort(in_ary)
    #return sorted(in_ary)

def my_count_sort(in_ary):
    if len(in_ary) <= 1:
        return in_ary
    k = max(in_ary)
    c = [0] * (k + 1)
    for item in in_ary:
        c[item] += 1
    for i in xrange(1, k+1):
        c[i] += c[i-1]
    out = [0] * len(in_ary)
    for item in in_ary:
        out[c[item] - 1] = item
    return out

class TestSomething(unittest2.TestCase):

    def assert_sort(self, in_ary, expected_out):
        self.assertEquals(expected_out, count_sort(in_ary))

    def test_something(self):
        self.assert_sort([], [])
        self.assert_sort([1], [1])
        self.assert_sort([1, 2], [1, 2])
        self.assert_sort([2, 1], [1, 2])
        self.assert_sort([2, 3, 1], [1, 2, 3])
        self.assert_sort(range(9, 0, -1), range(1, 10))
        self.assert_sort(range(999999, 0, -1), range(1, 1000000))
