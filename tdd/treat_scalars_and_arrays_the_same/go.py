import unittest2

def first_arg_list_to_scalar(retval_aggregator):
    def decorator(f):
        def method_replacement(self, *args, **kwargs):
            if isinstance(args[0], list):
                # TODO: test decorating a function instead of a method
                # TODO: all the selfs here are weird since this method isn't in a class
                def invoker(x):
                    newargs = []
                    newargs.append(x)
                    if len(args) > 1:
                        newargs.append(args[1:])
                    return f(self, *newargs, **kwargs)
                return reduce(retval_aggregator, map(invoker, args[0]))
            return f(self, *args, **kwargs)
        return method_replacement
    return decorator

def summer(arg1, arg2):
    return arg1 + arg2

# TODO: what if the function doesn't have a return value? then we don't need the retval_aggregator.

class TestSomething(unittest2.TestCase):

    @first_arg_list_to_scalar(summer)
    def one_arg_method(self, arg):
        return arg

    def two_arg_method(self, arg1, arg2):
        # TODO: these are so similar, but how to dedup them? also the one above
        # note they affect control flow...
        # decorator?
        if isinstance(arg1, list):
            return reduce(summer, map(lambda x: self.two_arg_method(x, arg2), arg1))

        if isinstance(arg2, list):
            return reduce(summer, map(lambda x: self.two_arg_method(arg1, x), arg2))

        return summer(arg1, arg2)

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
