import unittest2
import functools


# From https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer

@memoize
def get_count(num_digits, starting_at=1):
    # Return the count of numbers with num_digits numbers where each digit is >= the previous digit.
    # For example, 111 is ok, 112 is ok, 221 is not ok.
    if num_digits == 0:
        return 1
    ret = 0
    for i in range(starting_at, 10):
        ret += get_count(num_digits-1, i)
    return ret


class TestSomething(unittest2.TestCase):
    def test_something(self):
        self.assertEquals(9, get_count(1))
        self.assertEquals(45, get_count(2))
        self.assertEquals(165, get_count(3))
        self.assertEquals(495, get_count(4))
        self.assertEquals(1287, get_count(5))
        self.assertEquals(3003, get_count(6))

    def test_speed(self):
        # This function finishes in 0.16 seconds if get_count is memoized, and takes >1 minute (all I waited) without the memoization.
        self.assertEquals(352025629371, get_count(100))
