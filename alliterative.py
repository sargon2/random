#!/usr/bin/python

from __future__ import division
import sys
from collections import defaultdict

def get_max(str):
    letters = defaultdict(lambda: 0)
    max = 0
    for letter in str:
        v = letters[letter]
        v += 1
        letters[letter] = v
        if v > max:
            max = v
    return max

if __name__ == "__main__":
    with open("/usr/share/dict/words") as f:
        for line in f:
            str = line.strip()
            m = get_max(str)
            print m / len(str), m, len(str), str
