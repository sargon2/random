import unittest2

class TestSomething(unittest2.TestCase):

    def summer(self, arg1, arg2):
        return arg1 + arg2

    def one_arg_method(self, arg):
        if isinstance(arg, list):
            return reduce(self.summer, map(self.one_arg_method, arg))
        return arg

    def two_arg_method(self, arg1, arg2):
        # TODO: these are so similar, but how to dedup them? also the one above
        # note they affect control flow...
        if isinstance(arg1, list):
            return reduce(self.summer, map(lambda x: self.two_arg_method(x, arg2), arg1))

        if isinstance(arg2, list):
            return reduce(self.summer, map(lambda x: self.two_arg_method(arg1, x), arg2))

        return self.summer(arg1, arg2)

    def test_one_arg(self):
        # The idea here is if method is defined the same, method(list) should iterate and method(arg) should run once.
        self.assertEquals(3, self.one_arg_method(3))
        self.assertEquals(3, self.one_arg_method([1, 2]))

    def test_two_args(self):
        # But then what about 2-arg methods?  method(list, list) should run list*list times.
        self.assertEquals(1 + 2, self.two_arg_method(1, 2))
        self.assertEquals(1 + 3 + 2 + 3, self.two_arg_method([1, 2], 3))
        self.assertEquals(1+3+2+3+2+3+2+4, self.two_arg_method([1, 2], [3, 4]))
        self.assertEquals(1+2+1+3, self.two_arg_method(1, [2, 3]))
