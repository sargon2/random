import math
import sys
import unittest

def factor(num):
    ''' num must have exactly 2 non-trivial factors '''
    s = int(math.sqrt(num))

    big = s
    small = s

    while small > 1:
        m = big * small
        if small % 100000 == 0:
            print "%s * %s = %s" % (small, big, m)
        if m == num:
            return [small, big]
        if m < num:
            big += 1
        else:
            small -= 1
    print "fail"

class Test(unittest.TestCase):
    def test_something(self):
        self.assertEquals([17, 19], factor(323))
        # self.assertEquals([1500450271, 5915587277], factor(8876044532898802067))
