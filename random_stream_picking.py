import unittest2

# Problem: Each day, you're given a new random number.  You can keep the one from yesterday or replace it with a new one (before you see the new one).
# Do you do the replacement?
# There are n days left.

def calc(n):
    # Return the boundary at which your current number should be replaced.
    # If your current number is less than the return value, do the replace.
    if n == 0:
        return 0.0
    next_day = calc(n-1)
    return ((1-next_day) * (1+next_day) / 2) + next_day * next_day

class TestSomething(unittest2.TestCase):
    def test_something(self):
        self.assertAlmostEqual(calc(1), 0.5)
        self.assertAlmostEqual(calc(2), 0.625)
        self.assertAlmostEqual(calc(3), 0.6953125)
        self.assertAlmostEqual(calc(4), 0.741729736328125)
