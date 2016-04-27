#!/usr/bin/python

import unittest2
import math

def sierpinski(level):
    level = int(math.pow(2, level))
    ret = ''
    for i in range(level-1, -1, -1):
        ret += ' '*i
        for j in range(0, level):
            ret += '  ' if i & j else ' .'
        ret = ret.rstrip() + '\n'
    return ret

class TestSierpinski(unittest2.TestCase):
    def assertOutput(self, level, output):
        actual = sierpinski(level)
        self.assertEquals(output, actual)

    def test_whatever(self):
        self.assertOutput(0, ' .\n')

        self.assertOutput(1, '  .\n'
                           + ' . .\n'
                           )
        self.assertOutput(2, '    .\n'
                           + '   . .\n'
                           + '  .   .\n'
                           + ' . . . .\n'
                           )
        self.assertOutput(3, '        .\n'
                           + '       . .\n'
                           + '      .   .\n'
                           + '     . . . .\n'
                           + '    .       .\n'
                           + '   . .     . .\n'
                           + '  .   .   .   .\n'
                           + ' . . . . . . . .\n'
                           )

if __name__ == '__main__':
    print sierpinski(6)

