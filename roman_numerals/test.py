# http://langrsoft.com/jeff/2011/09/tdd-kata-roman-number-converter/

import unittest2
from collections import OrderedDict

class TestThings(unittest2.TestCase):

    def convert(self, arabic):
        d = {1: "I", 4: "IV", 5: "V", 9: "IX", 10: "X", 40: "XL", 50: "L", 90: "XC", 100: "C", 400: "CD", 500: "D", 900: "CM", 1000: "M"}

        result = ""

        for (arabicn, roman) in sorted(d.items(), reverse=True):
            result += roman * (arabic / arabicn)
            arabic = arabic % arabicn
        return result

    def assertNum(self, arabic, roman):
        self.assertEquals(roman, self.convert(arabic))

    def testThing(self):
        self.assertNum(1, "I")
        self.assertNum(2, "II")
        self.assertNum(3, "III")
        self.assertNum(10, "X")
        self.assertNum(20, "XX")
        self.assertNum(30, "XXX")
        self.assertNum(11, "XI")
        self.assertNum(33, "XXXIII")
        self.assertNum(23, "XXIII")
        self.assertNum(5, "V")
        self.assertNum(50, "L")
        self.assertNum(4, "IV")
        self.assertNum(9, "IX")
        self.assertNum(40, "XL")
        self.assertNum(2499, "MMCDXCIX")
        self.assertNum(3949, "MMMCMXLIX")
        self.assertNum(1904, "MCMIV")
        self.assertNum(2014, "MMXIV")
