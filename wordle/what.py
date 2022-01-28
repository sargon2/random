#!/usr/bin/env python3

import unittest
from collections import defaultdict

def get_matches(word1, word2):
    word1 = list(word1)
    word2 = list(word2)
    yellow = 0
    green = 0
    for i in range(0, 5):
        if word1[i] == word2[i]:
            green += 1
            word1[i] = None
            word2[i] = None
    for i in range(0, 5):
        letter = word1[i]
        if letter is None:
            continue
        pos = word2.index(letter) if letter in word2 else -1
        if pos >= 0:
            yellow += 1
            word2[pos] = None
            word1[i] = None
    return yellow, green

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
        self.assertMatches("abcde", "aabcd", 3, 1)
        self.assertMatches("abcde", "abcdd", 0, 4)
        self.assertMatches("aabcd", "xxxxa", 1, 0)

        # https://fivethirtyeight.com/features/can-you-design-the-perfect-wedding/
        self.assertMatches("magic", "misos", 1, 1)
        self.assertMatches("maims", "misos", 1, 2)
        self.assertMatches("sumps", "misos", 2, 1)
        self.assertMatches("mosso", "misos", 2, 2)
        self.assertMatches("misos", "misos", 0, 5)


def file_lines(filename):
    with open(filename) as f:
        return f.read().splitlines()

def main():
    results = defaultdict(lambda: 0)
    for word1 in file_lines("wordle-answers-alphabetical.txt"):
        for word2 in file_lines("wordle-answers-alphabetical.txt"):
            if word1 == word2:
                continue
            (yellow, green) = get_matches(word1, word2)
            results[word1] += (green + yellow) * 10000 + green
    for k, v in results.items():
        print(v, k)

if __name__ == "__main__":
    main()
