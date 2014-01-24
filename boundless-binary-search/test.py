import unittest2
import math

def negative(num):
    return -num

def linear(num):
    return num

def square(num):
    return math.pow(num, 2)

def searchFor(method, output):
    min = 0
    max = 1

    if method(min) == output:
        return min
    while(method(max) < output):
        max *= 2
    if method(max) == output:
        return max
    return normalBinarySearch(method, output, min, max)

def normalBinarySearch(method, output, min, max):
    done = False
    result = None
    while not done:
        guess = (min+max)/2.0
        oldresult = result
        result = method(guess)
        if oldresult == result or result == output:
            done = True
        elif result < output:
            min = guess
        else:
            max = guess

    return guess

class TestBoundlessBinarySearch(unittest2.TestCase):
    # to test:
    def test_square(self):
        self.assertEquals(2, searchFor(square, 4))
        self.assertEquals(3, searchFor(square, 9))
        self.assertEquals(1593, searchFor(square, 1593*1593))
        self.assertAlmostEqual(139.230025, searchFor(square, 19385), 6)
        self.assertEquals(1, searchFor(square, 1))
        self.assertEquals(0, searchFor(square, 0))
        self.assertEquals(0.5, searchFor(square, 0.25))

    # It turns out doing negative numbers is hard.  We have to do some detection on the method
    # to see if it's /, \, V, or ^ around the origin.

    # So, for now, it must be monotonically increasing.

    #def test_linear(self):
    #    self.assertEquals(-1, searchFor(linear, -1))
    #    self.assertEquals(-0.5, searchFor(linear, -0.5))
    #    self.assertEquals(-2, searchFor(linear, -2))

    #def test_negative(self):
    #    self.assertEquals(0, searchFor(negative, 0))
    #    self.assertEquals(1, searchFor(negative, -1))
    #    self.assertEquals(-1, searchFor(negative, 1))
    #    self.assertEquals(2, searchFor(negative, -2))
    #    self.assertEquals(-2, searchFor(negative, 2))
    #    self.assertEquals(0.5, searchFor(negative, -0.5))
    #    self.assertEquals(-0.5, searchFor(negative, 0.5))
