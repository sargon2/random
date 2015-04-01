import unittest2

def aggregate_arg(retval_aggregator, argnum):  # TODO: name
    # note that if the decorated method is in a class, self is argnum 0
    def decorator(f):
        def method_replacement(*args, **kwargs):
            if isinstance(args[argnum], list):
                # TODO: test decorating a function instead of a method
                def invoker(x):
                    newargs = list(args[:])
                    newargs[argnum] = x
                    return f(*newargs, **kwargs)
                return reduce(retval_aggregator, map(invoker, args[argnum]))
            return f(*args, **kwargs)
        return method_replacement
    return decorator

def summer(arg1, arg2): # TODO: what if you want to specify this in the class? is that possible?
    return arg1 + arg2

# TODO: what if the function doesn't have a return value? then we don't need the retval_aggregator.

class TestSomething(unittest2.TestCase):

    @aggregate_arg(summer, 1)
    def one_arg_method(self, arg):
        return arg

    @aggregate_arg(summer, 1)
    @aggregate_arg(summer, 2)
    def two_arg_method(self, arg1, arg2):
        return arg1 + arg2

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
