#!/usr/bin/python
# coding=utf-8

def read_known_kanji():
    with open("known-kanji.txt") as f:
        chars = f.read()
        return list(chars.decode('utf-8').strip())

if '私'.decode('utf-8') in read_known_kanji():
    print "found!"
