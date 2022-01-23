#!/usr/bin/env python3

import unittest
from collections import defaultdict

def get_matches(word1, word2):
    yellow = 0
    green = 0
    for i in range(0, 5):
        if word1[i] == word2[i]:
            green += 1
    for letter in word1:
        if letter in word2:
            yellow += 1
    yellow -= green
    return yellow, green

def has_repeated_letters(word):
    for letter in word:
        if word.count(letter) > 1:
            return True
    return False


class TestGetMatches(unittest.TestCase):
    def assertMatches(self, word1, word2, yellow, green):
        (actual_y, actual_g) = get_matches(word1, word2)
        self.assertEqual(yellow, actual_y)
        self.assertEqual(green, actual_g)

    def test_get_matches(self):
        self.assertMatches("aaaaa", "aaaaa", 0, 5)
        self.assertMatches("aaaab", "aaaaa", 0, 4)
        self.assertMatches("abcde", "xaxxx", 1, 0)
        self.assertMatches("abcde", "axbxx", 1, 1)
        self.assertMatches("abcde", "abced", 2, 3)
        # TODO There is some weirdness with repeated letters that I'm ignoring for now.

    def test_has_repeated_letters(self):
        self.assertEqual(False, has_repeated_letters("abcde"))
        self.assertEqual(True, has_repeated_letters("aabcd"))


def file_lines(filename):
    with open(filename) as f:
        return f.readlines()

def main():
    results = defaultdict(lambda: 0)
    for word1 in file_lines("wordle-answers-alphabetical.txt"):
        if has_repeated_letters(word1):
            continue
        for word2 in file_lines("wordle-answers-alphabetical.txt"):
            if has_repeated_letters(word2):
                continue
            if word1 == word2:
                continue
            (yellow, green) = get_matches(word1, word2)
            results[word1] += (green + yellow) * 10000 + green
    for k, v in results.items():
        print(v, k)

if __name__ == "__main__":
    main()
