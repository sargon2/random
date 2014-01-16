import unittest

import digit_factor

class TestDigitFactor(unittest.TestCase):
    def assertResult(self, i, j):
        self.assertEquals(sorted((i, j)), sorted(digit_factor.factor(i * j)))
    def test_2_2(self):
        self.assertResult(2, 2)
    def test_5_7(self):
        self.assertResult(5, 7)
    def test_23_23(self):
        self.assertResult(23, 23)
    def test_23_31(self):
        self.assertResult(23, 31)
    def test_23_89(self):
        self.assertResult(23, 89)
    def test_367_367(self):
        self.assertResult(367, 367)
    def test_367_373(self):
        self.assertResult(367, 373)
    def test_2851_2851(self):
        self.assertResult(2851, 2851)
    def test_5051_5059(self):
        self.assertResult(5051, 5059)
    def test_55619_55621(self):
        self.assertResult(55619, 55621)
    def test_10007_10009(self):
        self.assertResult(10007, 10009)
