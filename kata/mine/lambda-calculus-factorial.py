# 1. Write factorial recursively.
# 2. Convert it to anonymous recursion.  It should have no named functions.
# 3. Convert it to lambda calculus.  It should have no functions that take more than one argument.
#
# Hint: http://en.wikipedia.org/wiki/Anonymous_recursion

def factorial(n):
    return step_3(n)

def step_1(n):
    if n == 0:
        return 1
    return n * factorial(n-1)

step_2 = (lambda f: lambda x: f(f, x))(lambda f, x: 1 if x == 0 else x * f(f, x-1))

step_3 = (lambda f: lambda x: f(f)(x))(lambda f: lambda x: 1 if x == 0 else x * f(f)(x-1))

# Step 3 was easy, I just replaced lambda a, b with lambda a: lambda b:, and (a, b) with (a)(b).

# Note that my solution is simpler than the one on wikipedia.  Go TDD.

import unittest2

class TestFactorial(unittest2.TestCase):
    def test_something(self):
        self.assertEquals(1, factorial(0))
        self.assertEquals(1, factorial(1))
        self.assertEquals(2, factorial(2))
        self.assertEquals(6, factorial(3))
        self.assertEquals(24, factorial(4))
