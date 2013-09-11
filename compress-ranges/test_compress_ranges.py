import unittest

import compress_ranges

class TestCompressRanges(unittest.TestCase):
    def assertRangeString(self, expected, input):
        self.assertEqual(expected, str(compress_ranges.Ranges(input)))

    def testAssertRangeStringFail(self):
        try:
            self.assertRangeString("1", [2])
        except AssertionError:
            pass
        else:
            self.fail("expected a failure")

    def testRangeString(self):
        self.assertRangeString("1", [1])
        self.assertRangeString("1", [1, 1])
        self.assertRangeString("1", ["1"])
        self.assertRangeString("1", ["01"])
        self.assertRangeString("1-2", ["1", "2"])
        self.assertRangeString("1-4", ["1-2", "3-4"])
        self.assertRangeString("1-4", ["1-2", "1-4"])
        self.assertRangeString("1-4", ["1-4", "3-4"])
        self.assertRangeString("1-4", ["2-4", "1-3"])
        self.assertRangeString("1-2, 4-5", ["1-2", "4-5"])
        self.assertRangeString("1-2", [1, 2])
        self.assertRangeString("1-2", [2, 1])
        self.assertRangeString("1, 3", [1, 3])
        self.assertRangeString("1, 3", [3, 1])
        self.assertRangeString("1, 3-4", [1, 3, 4])
        self.assertRangeString("", [])
        self.assertRangeString("", None)
        self.assertRangeString("1-11", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])
