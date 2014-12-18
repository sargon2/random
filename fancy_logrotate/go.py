import unittest2
from collections import defaultdict

# The idea here is we keep old logs, and progressively delete them as they get older.
# We always keep the oldest log.
# The older a log is, the more likely it is to be deleted.
# This makes the space the logs take up about log(num of logs). No pun intended.

def calculate(booldict):
    m = max(booldict.keys())
    i = 0
    r = 1
    while i <= m:
        c = False
        # 0
        # 2, 1
        # 6, 5, 4, 3
        # 14, 13, 12, 11, 10, 9, 8, 7
        maxc = i*2
        minc = i
        for j in range(maxc, minc-1, -1):
            if booldict[j]:
                if c:
                    booldict[j] = False
                c = True
        i += r
        r *= 2

    return booldict

def convert_str_to_defaultdict(instr):
    ret = defaultdict(lambda: False)
    for i, char in enumerate(instr):
        if char == "X":
            ret[i] = True
    return ret

def convert_defaultdict_to_str(indict):
    ret = ""
    m = max(indict.keys())
    for i in range(0, m+1):
        if indict[i]:
            ret += "X"
        else:
            ret += " "
    return ret.rstrip()

def calculate_str(instr):
    to_pass = convert_str_to_defaultdict(instr)
    output = calculate(to_pass)
    str_out = convert_defaultdict_to_str(output)
    return str_out

class TestLogRotate(unittest2.TestCase):

    def assert_str(self, test_input, expected_output, msg = None):
        output = calculate_str(test_input)
        self.assertEquals(output, expected_output, msg = msg)

    def test_assert_str_fails(self):
        with self.assertRaises(AssertionError):
            self.assert_str("X", "XXXX")

    def test_progression(self):
        # We divide the history of logs into groups.
        # There's a group of size 1, then 2, then 4, then 8, etc.
        # We only keep one log in each group (the oldest we've seen).
        expected_progression = [
           # |..||||........||||||||||||||||.
            "X",
            "XX",
            "X X",
            "XX X",
            "X X X",
            "XX   X",
            "X X   X",
            "XX X   X",
            "X X X   X",
            "XX   X   X",
            "X X   X   X",
            "XX X       X",
            "X X X       X",
            "XX   X       X",
            "X X   X       X",
            "XX X   X       X",
            "X X X   X       X",
        ]

        prev_item = ""
        for item in expected_progression:
            test_input = "X" + prev_item
            self.assert_str(test_input, item, test_input + " -> " + item)
            prev_item = item

    def test_non_progression(self):
        self.assert_str("XXXXXXXXXXXXXXX", "X X   X       X")
        self.assert_str("XXXXXXXXXXXXXX",  "X X   X      X")

# TODO: actually rotate logs (parse their filenames or timestamps, etc)
if __name__ == "__main__":
    s = "X"
    for i in range(1, 100):
        result = calculate_str(s)
        print result
        s = "X" + result
