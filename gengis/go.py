#!/usr/bin/python


# http://forum.codecall.net/blog/1699/entry-1992-another-fun-programming-exercise-genghis-kahn-the-problem/

# Solution: https://oeis.org/A006257

import unittest2
import math

class TestGengis(unittest2.TestCase):
    def rot_binary(self, binary):
        if len(binary) == 1:
            return binary
        return binary[1:] + binary[0]

    def calc_gengis(self, num_men):
        """ I tested this with some big integers (>1000 digits) and it returned instantly.  This is the fastest implementation I know of. """
        binary = bin(num_men)[2:]
        binary = self.rot_binary(binary)
        return int(binary, 2)

    def assert_gengis(self, num_men, expected_result):
        self.assertEquals(expected_result, self.calc_gengis(num_men))

    def test_rot(self):
        self.assertEquals("1", self.rot_binary("1"))
        self.assertEquals("01", self.rot_binary("10"))
        self.assertEquals("11", self.rot_binary("11"))
        self.assertEquals("001", self.rot_binary("100"))
        self.assertEquals("101", self.rot_binary("110"))
        self.assertEquals("0001", self.rot_binary("1000"))
        self.assertEquals("1001", self.rot_binary("1100"))

    def test_gengis(self):
        self.assert_gengis(0, 0) # by definition
        self.assert_gengis(1, 1)
        self.assert_gengis(2, 1)
        self.assert_gengis(3, 3)
        self.assert_gengis(4, 1)
        self.assert_gengis(5, 3)
        self.assert_gengis(6, 5)
        self.assert_gengis(7, 7)
        self.assert_gengis(8, 1)
        self.assert_gengis(1000, 977) # I hope...
