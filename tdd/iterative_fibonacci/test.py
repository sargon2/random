import unittest2

class TestIterativeFibonacci(unittest2.TestCase):
    def fib(self, inval):
        fiba, fibb = 0, 1
        for i in range(inval):
            fiba, fibb = fibb, fiba + fibb
        return fibb

    def assert_fib(self, inval, expected):
        self.assertEquals(expected, self.fib(inval))

    def test_fib(self):
        self.assert_fib(0, 1)
        self.assert_fib(1, 1)
        self.assert_fib(2, 2)
        self.assert_fib(3, 3)
        self.assert_fib(4, 5)
        self.assert_fib(5, 8)
        self.assert_fib(6, 13)
        self.assert_fib(7, 21)

    def test_large_number(self):
        self.fib(10000) # less than .009 seconds
