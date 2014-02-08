
import unittest

class Test(unittest.TestCase):

    def dtest_add(self):
        return (self.add, [(3,    [1, 2]),
                           (0,    [0, 0]),
                           (0,    [0, 0, 0]),
                           (0,    [0]),
                           ("a",  ["a"]),
                           ("ab", ["a", "b"]),
                          ]
               )

    def dtest_subtract(self):
        return (self.subtract, [(0, [0, 0]),
                                (0, [0]),
                                (1, [3, 2]),
                                (1, [3, 1, 1]),
                                (2, [5, 2, 1]),
                               ]
               )

    def add(self, nums):
        return reduce(lambda x, y: x + y, nums)

    def subtract(self, nums):
        return reduce(lambda x, y: x - y, nums)

    def test_dtest_methods(self):
        # TODO: automatically discover methods to call
        # TODO: *args, **kwargs
        methods = [self.dtest_add, self.dtest_subtract]
        for method in methods:
            (method_name, method_values) = method()
            for (key, value) in method_values:
                self.assertEquals(key, method_name(value))
