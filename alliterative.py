#!/usr/bin/python

from __future__ import division
import sys
from collections import defaultdict

def get_counts(str):
    letters = defaultdict(lambda: 0)
    for letter in str:
        letters[letter] += 1
    return letters

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "return the alliterative index of a string"
        print "usage:", sys.argv[0], "<str>"
        sys.exit()
    str = sys.argv[1]
    counts = get_counts(str)
    s = sorted(counts, key=counts.get, reverse=True)
    m = counts[s[0]]
    print m / len(str), str
