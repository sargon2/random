# http://icfpcontest.org/spec.html
# Bishop said rotating on a hex grid is hard, so I thought I'd try it.

# 0,0   1,0   2,0   3,0   4,0
#    0,1   1,1   2,1   3,1   4,1
# 0,2   1,2   2,2   3,2   4,2
#    0,3   1,3   2,3   3,3   4,3
# 0,4   1,4   2,4   3,4   4,4
#    0,5   1,5   2,5   3,5   4,5

import unittest2

class TestHexRotate(unittest2.TestCase):
    def rotate(self, pivot, point):
        (x, y) = pivot
        (a, b) = point

        X = a-x
        Y = b-y

        # http://gamedev.stackexchange.com/a/55493
        # Switch coordinate systems
        xx = X - (Y - (Y&1)) / 2
        zz = Y
        yy = -xx - zz

        # Do rotation
        # xx, yy, zz = -zz, -xx, -yy # rotate clockwise
        xx, yy, zz = -yy, -zz, -xx # rotate counterclockwise

        # Switch back
        X = xx + (zz - (zz&1)) / 2
        Y = zz

        return (X+x, Y+y)

    def test_noop(self):
        self.assertEquals((2, 2), self.rotate((2, 2), (2, 2)))

    def test_33(self):
        self.assertEquals((3, 3), self.rotate((3, 4), (4, 4)))

    def test_circle_around_22(self):
        self.assertEquals((3, 2), self.rotate((2, 2), (2, 3)))
        self.assertEquals((2, 1), self.rotate((2, 2), (3, 2)))
        self.assertEquals((1, 1), self.rotate((2, 2), (2, 1)))
        self.assertEquals((1, 2), self.rotate((2, 2), (1, 1)))
        self.assertEquals((1, 3), self.rotate((2, 2), (1, 2)))
        self.assertEquals((2, 3), self.rotate((2, 2), (1, 3)))

    def test_horizontal(self):
        self.assertEquals((3, 0), self.rotate((2, 2), (4, 2)))
        self.assertEquals((3, -1), self.rotate((2, 2), (5, 2)))
        self.assertEquals((1, 4), self.rotate((2, 2), (0, 2)))
        self.assertEquals((2, 4), self.rotate((3, 2), (1, 2)))
        self.assertEquals((2, 4), self.rotate((4, 0), (0, 0)))
