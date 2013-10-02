
import unittest
import re

class DoIt(object):
    def go(self):
        r = []
        day_nums = []
        with open("weather.dat") as f:
            for line in f:
                parts = self.parse_line(line, 0, 1, 2)
                if parts is not None:
                    r.append((parts[1], parts[2]))
                    day_nums.append(parts[0])
        index = self.find_smallest_spread(r)
        print day_nums[index]

    def find_smallest_spread(self, input):
        smallest = None
        retval = None
        i = 0
        for (low, high) in input:
            spread = abs(high - low)
            if smallest is None or spread < smallest:
                smallest = spread
                retval = i
            i += 1
        return retval

    def getint(self, str):
        return int(''.join(c for c in str if c.isdigit()))

    def parse_line(self, line, *fields):
        line = re.split('\s+', line.strip())
        try:
            r = []
            for field in fields:
                r.append(self.getint(line[field]))
            return tuple(r)
        except:
            return None


class Test(unittest.TestCase):

    def test_something(self):
        input1 = (1, 2)
        input2 = (2, 4)
        self.assertEquals(0, DoIt().find_smallest_spread([input1, input2]))

    def test_reverse(self):
        input1 = (2, 1)
        input2 = (4, 2)
        self.assertEquals(0, DoIt().find_smallest_spread([input1, input2]))

    def test_something_else(self):
        input1 = (1, 5)
        input2 = (5, 7)
        input3 = (8, 9)
        self.assertEquals(2, DoIt().find_smallest_spread([input1, input2, input3]))

    def test_parse_line(self):
        self.assertEquals((1, 2), DoIt().parse_line("1 2", 0, 1))
        self.assertEquals((1, 2), DoIt().parse_line(" \t 1  \t 2 \t ", 0, 1))
        self.assertEquals((1, 2), DoIt().parse_line("1 2 3", 0, 1))
        self.assertEquals((1, 3), DoIt().parse_line("1 2 3", 0, 2))
        self.assertEquals((2, 3), DoIt().parse_line("1 2 3", 1, 2))
        self.assertEquals(None, DoIt().parse_line("1", 0, 1))
        self.assertEquals((1, 2), DoIt().parse_line("1* 2", 0, 1))
        self.assertEquals((1, 2, 3), DoIt().parse_line("1 2 3", 0, 1, 2))


if __name__ == "__main__":
    t = DoIt()
    t.go()
