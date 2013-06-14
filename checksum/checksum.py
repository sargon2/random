import unittest

def get_checksum(item):
    s = str(item)
    total = 0
    r = 1
    for digit in s:
        total += int(digit) * r
        r *= 2
    print "for " + str(item) + ", returning " + str(total)
    if(len(str(total)) > 2):
        return get_checksum(total)
    return total

def get_checksums(*args):
    return [get_checksum(x) for x in args]

class test(unittest.TestCase):

    def assert_checksum_different(self, a, b):
        (ca, cb) = get_checksums(a, b)
        self.assertFalse(ca == cb)

    def assert_checksum_same(self, a, b):
        (ca, cb) = get_checksums(a, b)
        self.assertTrue(ca == cb)

    def testSomething(self):
        self.assert_checksum_same(1, 1)
        self.assert_checksum_different(1, 2)
        self.assert_checksum_different(12, 21)
        self.assert_checksum_different(12, 13)
        self.assert_checksum_different(111112, 111113)
        self.assertTrue(len(str(get_checksum(123456789))) <= 2)
        self.assert_checksum_different(121111, 114111)
        self.assert_checksum_different(12, 31)
