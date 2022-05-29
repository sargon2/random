#!/usr/bin/env python3

import unittest

class TestSomething(unittest.TestCase):
    def test_something():
        assertIAmHappy()
        assertIAmRich() # fails
        # but why do I want to be rich? <-- this is important
        assertIDontHaveToWork() # fails
        assertGoodIncome() # passes right now
        assertIHaveTimeAffluence() # fails

    def assertIAmHappy():
        # What do I need to be happy?

    def assertRich():
        # Being rich consists of two things: net worth, and yearly income.
        assertNetWorthGreaterThan(...)
        assertGoodYearlyIncome()

    def assertGoodYearlyIncome():
        # Having a good yearly income consists of two things: the amount, and the reliability.
        fail()

    def assertIncomeReliability():
        # Number of streams, how reliable is each stream, the reliability of the currency itself
        fail()


