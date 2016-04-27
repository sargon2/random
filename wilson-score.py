# http://www.evanmiller.org/how-not-to-sort-by-average-rating.html
# http://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval

from __future__ import division

import unittest2
from math import sqrt

def getScore(positive, total):
    # TODO: calculate z from confidence
    z = 1.96 # 95%
    if total == 0:
        return 0
    p_hat = positive/total
    return (p_hat + z*z/(2*total) - z * sqrt((p_hat*(1-p_hat)+z*z/(4*total))/total))/(1+z*z/total)

class TestWilson(unittest2.TestCase):

    def assertBetter(self, positive1, total1, positive2, total2):
        self.assertGreater(getScore(positive1, total1), getScore(positive2, total2), msg = "%s/%s vs %s/%s" % (positive1, total1, positive2, total2))

    def test_ordering(self):
        self.assertBetter(90, 100, 89, 100)
        self.assertBetter(999, 1000, 1, 1)
        self.assertBetter(90, 100, 100, 200)

    def test_corner_cases(self):
        self.assertEquals(0, getScore(0, 0))
        self.assertEquals(0, getScore(1, 0))
