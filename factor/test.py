import unittest
import math

class TestGetPrimeFactors(unittest.TestCase):
    def get_prime_factors(self, input):
        ret = []
        d = 2
        while input > 1:
            while input % d == 0:
                ret.append(d)
                input /= d
            d += 1
            if d*d > input:
                if input > 1:
                    ret.append(input)
                break
        return ret

    def assert_prime_factors(self, expected, input):
        result = self.get_prime_factors(input)
        self.assertEquals(expected, result)

    def test_get_prime_factors(self):
        self.assert_prime_factors([], 1)
        self.assert_prime_factors([2], 2)
        self.assert_prime_factors([3], 3)
        self.assert_prime_factors([2, 3], 6)
        self.assert_prime_factors([2, 2, 3], 12)
        # We ensure it has a good run time by testing some bigger numbers.
        # I think it runs in O(sqrt(n)).
        self.assert_prime_factors([5, 5, 11, 332191], 91352525)
        self.assert_prime_factors([2, 3, 5, 7, 11, 13, 17, 19], 9699690)
        self.assert_prime_factors([2, 3, 5, 7, 11, 13, 17, 19, 23], 223092870)
        self.assert_prime_factors([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], 6469693230)
        self.assert_prime_factors([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31], 200560490130)
        self.assert_prime_factors([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37], 7420738134810)
        self.assert_prime_factors([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41], 304250263527210)
        self.assert_prime_factors([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43], 13082761331670030)
        self.assert_prime_factors([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47], 614889782588491410)
        self.assert_prime_factors([953, 46727, 13808181181], 614889782588491411)
        self.assert_prime_factors([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71], 557940830126698960967415390)
        self.assert_prime_factors([5915587277], 5915587277)
