#!/usr/bin/python
import unittest2
from collections import defaultdict
import re
import random

def align(str):
    # I'm pretty sure the fastest we can do this is O(n^2).  Think of the case of all \ - we're rendering n^2/2 characters.

    # This is insanely complicated because I wasn't able to properly TDD it.  I just wrote the solution up front.
    world = defaultdict(lambda: [' '] * len(str))
    x = y = 0
    min_y = max_y = 0
    for char in str:
        if char == '\\' and x != 0:
            y += 1

        world[y][x] = char
        min_y = min(min_y, y)
        max_y = max(max_y, y)

        if char == '/':
            y -= 1

        x += 1

    lines = ["".join(world[i]) for i in range(min_y, max_y+1)]
    ret = "\n".join(lines).rstrip()
    ret = re.sub(' +\n', '\n', ret)
    return ret

class TestAlign(unittest2.TestCase):
    def assertAlign(self, expected, input):
        self.assertEquals(expected, align(input))

    def test_one_char(self):
        self.assertAlign("_", "_")
        self.assertAlign("/", "/")
        self.assertAlign("\\", "\\")

    def test_two_chars(self):
        self.assertAlign(" _\n/", "/_")
        self.assertAlign(" /\n/", "//")
        self.assertAlign("/\\", "/\\")

        self.assertAlign("__", "__")
        self.assertAlign("_/", "_/")
        self.assertAlign("_\n \\", "_\\")

        self.assertAlign("\\_", "\\_")
        self.assertAlign("\\/", "\\/")
        self.assertAlign("\\\n \\", "\\\\")

    def test_three_chars(self):
        self.assertAlign("  /\n /\n/", '///')
        self.assertAlign("\\\n \\\n  \\", '\\\\\\')

    def test_up_and_down(self):
        self.assertAlign(" _   _   _   _\n/ \\_/ \\_/ \\_/ \\", "/_\\_/_\\_/_\\_/_\\")

def generate():
    chars = ['/', '_', '\\']
    ret = ""
    for i in range(1, 80):
        ret += random.sample(chars, 1)[0]
    return ret

if __name__ == "__main__":
    print(align(generate()))
