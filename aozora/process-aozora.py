#!/usr/bin/python
# coding=utf-8

from __future__ import division
import os
from collections import defaultdict

def get_data(filename):
    with open(filename) as f:
        chars = f.read()
        return set(chars.decode('utf-8').strip())

def read_known_kanji():
    ret = get_data("known-kanji.txt")
    ret |= get_data("other-known-chars.txt")
    return ret

kanji_freq = defaultdict(lambda: 0)
books = {}

known = read_known_kanji()

def is_known(char):
    return char in known

def process(path):
    with open(path) as f:
        chars = f.read()
        chars = list(chars.decode('shift_jis', errors='ignore'))
        known = 0
        unknown = 0
        for item in chars:
            if item.strip() == "":
                continue
            if is_known(item):
                known = known + 1
                pass
            else:
                unknown = unknown + 1
                kanji_freq[item] += 1
        books[path] = 100 * known / (unknown + known)

for (dirpath, dirnames, filenames) in os.walk("textfiles"):
    for filename in filenames:
        f = os.path.join(dirpath, filename)
        print "Processing %s" % (f)
        process(f)

print "Characters you should learn:"
i=0
for key in sorted(kanji_freq, key=kanji_freq.get, reverse=True):
    i += 1
    print key, kanji_freq[key]
    if i > 30:
        break

print "Books you could read:"
i=0
for key in sorted(books, key=books.get, reverse=True):
    i += 1
    print key, books[key]
    if i > 30:
        break
