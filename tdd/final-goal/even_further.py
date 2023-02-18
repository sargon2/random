#!/usr/bin/env python3

import unittest
import datetime


class TestSomething(unittest.TestCase):
    def test_good_life(self):
        self.assertGoodLife()  # TODO name might not be quite right
        # But is it possible to have a good life?  Let's find out, I suppose.
        # But should I desire a good life? Buddhism says desire is the root of suffering.
        # Maybe that's just attachment to desire.

    def assertGoodLife(self):
        with self.subTest(msg="love"):  # Makes it keep running on failure
            self.assertLoveLife()
        with self.subTest(msg="money"):
            self.assertRich()  # but why do I want to be rich? <-- this is important
        with self.subTest(msg="entertainment"):
            self.assertEntertainment()
        with self.subTest(msg="friendship"):
            self.assertFriendship()

        with self.subTest(msg="philosophy"):
            self.assertPhilosophy()

        with self.subTest(msg="internal locus of control"):
            self.assertInternalLocusOfControl()

        with self.subTest(msg="time affluence"):
            self.assertTimeAffluence()

    def assertPhilosophy(self):
        # What we're asserting here is that philosophy is a part of my life and I have time for it.
        pass

    def assertLoveLife(self):
        # Do I have a love life that I'm happy with?

        # TODO break this down further
        self.fail("Not happy with love life")

    def assertInternalLocusOfControl(self):
        # This is a tough one right now.
        # If I have a boss, and he tells me what to do, and I do it, do I have an internal locus of control?
        # What if I want to take a vacation and he won't let me?
        # There is the strategy where when the boss tells me what to do, I simply add it to the discovery list of
        # what I could possibly do.  But that does mean if I don't do it, I owe him an explanation.
        self.fail("I do have an internal locus of control, but I haven't fully internalized it and related it to work/employment.")

    def xtest_ideas(self):
        # Ideas for things I could test that aren't actually executed right now
        self.assertHappy()  # It's impossible to be happy all the time.
        # Cannot continue to pass by definition since getting old sucks.
        self.assertMyLifeIsImproving()

        self.assertIHaveTimeAffluence()  # fails

    def assertIAmHappy(self):
        # What do I need to be happy?

        # It's impossible to be happy all the time.
        self.fail()

    def assertFriendship(self):
        # Do I have meaningful friendships?
        pass  # IRC friends are meaningful friends, right? right?

        # Do I have a mechanism to make new real-life friends?
        self.fail("No mechanism found to make new real-life friends")

    def assertTimeAffluence(self):
        # Do I feel like I control what I do with my time?
        # This was a fail last year, but I think moving my bedtime has helped a lot.
        # It's a tentative pass.
        self.pass_for_time(datetime.datetime(2023, 2, 18),
                           datetime.timedelta(days=30))

    def assertEntertainment(self):
        # Am I happy with the level of entertainment in my life?
        # Video games, tv shows, movies, youtube, real-life entertainment
        pass

    def assertRich(self):
        # Being rich consists of possibly two things: net worth, and yearly income.

        # Asserting my net worth is the true definition of rich for me.  But it
        # will fail right now.  Is it okay for it to fail? Then how do I assert it
        # will happen soon? Do I need to?
        self.assertNetWorth("USD", 40000000)  # TODO the number can be tuned

        # self.assertIDontHaveToWork() # fails

        # You might think a yearly income is important for being rich, but if you have enough net worth, that's taken care of.
        # So this assert is not needed. But, it would pass right now.
        # assertGoodIncome()

    def assertNetWorth(self, currency, amount):
        # Right now only USD is supported.
        self.assertEqual(currency, "USD")
        # Number is from mint and is approximate.
        self.assertGreater(800000, amount)
        self.pass_for_time(datetime.datetime(2023, 2, 18),
                           datetime.timedelta(months=4))

    def assertGoodIncome(self):
        # Having a good yearly income consists of two things: the amount, and the reliability.
        # As of today I do have a good income.
        self.pass_for_time(datetime.datetime(2023, 2, 18),
                           datetime.timedelta(months=4))

    def assertIncomeReliability(self):
        # Number of streams, how reliable is each stream, the reliability of the currency itself
        fail("Not written yet")

    def pass_for_time(self, start_time, duration):
        self.assertTrue(datetime.datetime.now() < start_time + duration, "pass_for_time expired")
