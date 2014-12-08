import unittest2

def calculate(instr):
    parts = instr.split("+")
    if len(parts) > 1:
        return sum([int(calculate(x)) for x in parts])
    parts = instr.split("-")
    if len(parts) > 1:
        ret = int(parts[0])
        for i in range(1, len(parts)):
            ret -= int(parts[i])
        return ret
    return int(parts[0])

class TestThings(unittest2.TestCase):
    def test_something(self):
        self.assertEquals(1, calculate("1"))
        self.assertEquals(2, calculate("2"))
        self.assertEquals(2, calculate("1 + 1"))
        self.assertEquals(6, calculate("1 + 2 + 3"))
        self.assertEquals(6, calculate("1+2+3"))
        self.assertEquals(6, calculate(" 01   +2+3"))
        self.assertEquals(1, calculate("3-2"))
        self.assertEquals(1, calculate("4-2-1"))
        self.assertEquals(4, calculate("3+2-1"))
        self.assertEquals(2, calculate("3-2+1"))
        # TODO: * / ! etc
