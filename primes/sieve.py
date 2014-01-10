
import unittest2
import time
from collections import defaultdict

# Witnesses have:
# - A base value
# - A current value
# We start i at 2. If i does not equal the smallest witness' current value:
# - It's prime
# - It becomes a new witness
# If it does equal a witness value:
# - That witness gets advanced

# So, store witnesses as witness[current_value] = base_value
# Then, to advance a witness:
# base_value = witness[current_value]
# witness[current_value + base_value] = base_value
# unset witness[current_value]

def sieve():
    yield 2
    witness = defaultdict(lambda: 0)
    i = 3
    while 1:
        if witness[i]:
            # Advance the witness to the next open multiple
            base_value = witness.pop(i)
            next_val = i + base_value
            while next_val in witness:
                next_val += base_value
            witness[next_val] = base_value
        else:
            yield i
            witness[i*i] = i*2 # I got this from the forum.  Why isn't it witness[i*2] = i?
        i += 2


class TestSieve(unittest2.TestCase):

    def assert_sieve_values(self, values):
        for (expected, actual) in zip(values, sieve()):
            print "(%s, %s)" % (expected, actual)
            self.assertEquals(expected, actual)

    def test_basic(self):
        self.assert_sieve_values([2])
        self.assert_sieve_values([2, 3])
        self.assert_sieve_values([2, 3, 5])
        self.assert_sieve_values([2, 3, 5, 7, 11])
        self.assert_sieve_values([2, 3, 5, 7, 11, 13, 17])

    def test_speed(self):

        # todo: with assertSpeed(.1):
        start = time.clock()
        for i in sieve():
            if i > 100000:
                break
        end = time.clock()
        elapsed = end - start
        self.assertLess(elapsed, .1)
