import unittest

from grammar import Regex, ZeroOrMore, ZeroOrOne

class TestGrammar(unittest.TestCase):
    def test_zeroorone_zero(self):
        z = ZeroOrOne("a")

        class grammar_provider:
            a = Regex("a")
        code_provider = None

        result = z.parse("", grammar_provider, code_provider)
        self.assertEqual(0, len(result))

    def test_zeroorone_one(self):
        z = ZeroOrOne("a")

        class grammar_provider:
            a = Regex("a")
        code_provider = None

        result = z.parse("a", grammar_provider, code_provider)
        self.assertEqual(1, len(result))
        self.assertEqual("a", result[0].literal_value)

    def test_zeroorone_zero_two_items(self):
        z = ZeroOrOne("a", "b")

        class grammar_provider:
            a = Regex("a")
            b = Regex("b")
        code_provider = None

        result = z.parse("", grammar_provider, code_provider)
        self.assertEqual(0, len(result))

    def test_zeroorone_one_two_items(self):
        z = ZeroOrOne("a", "b")

        class grammar_provider:
            a = Regex("a")
            b = Regex("b")
        code_provider = None

        result = z.parse("ab", grammar_provider, code_provider)
        self.assertEqual(2, len(result))
        self.assertEqual("a", result[0].literal_value)
        self.assertEqual("b", result[1].literal_value)

    def test_zeroormore_zero(self):
        z = ZeroOrMore("a")
        class grammar_provider:
            a = Regex("a")
        code_provider = None
        result = z.parse("", grammar_provider, code_provider)
        self.assertEqual(0, len(result))

    def test_zeroormore_one(self):
        z = ZeroOrMore("a")
        class grammar_provider:
            a = Regex("a")
        code_provider = None
        result = z.parse("a", grammar_provider, code_provider)
        self.assertEqual(1, len(result))
        self.assertEqual("a", result[0][0].literal_value) # two zeroes because the first one is overall group and the second is item within the group

    def test_zeroormore_two(self):
        z = ZeroOrMore("a")
        class grammar_provider:
            a = Regex("a")
        code_provider = None
        result = z.parse("aa", grammar_provider, code_provider)
        self.assertEqual(2, len(result))
        self.assertEqual("a", result[0][0].literal_value)
        self.assertEqual("a", result[1][0].literal_value)

    def test_zeroormore_zero_two_items(self):
        z = ZeroOrMore("a", "b")
        class grammar_provider:
            a = Regex("a")
            b = Regex("b")
        code_provider = None
        result = z.parse("", grammar_provider, code_provider)
        self.assertEqual(0, len(result))

    def test_zeroormore_one_two_items(self):
        z = ZeroOrMore("a", "b")
        class grammar_provider:
            a = Regex("a")
            b = Regex("b")
        code_provider = None
        result = z.parse("ab", grammar_provider, code_provider)
        self.assertEqual(1, len(result))
        self.assertEqual("a", result[0][0].literal_value)
        self.assertEqual("b", result[0][1].literal_value)

    def test_zeroormore_two_two_items(self):
        z = ZeroOrMore("a", "b")
        class grammar_provider:
            a = Regex("a")
            b = Regex("b")
        code_provider = None
        result = z.parse("abab", grammar_provider, code_provider)
        self.assertEqual(2, len(result))
        self.assertEqual("a", result[0][0].literal_value)
        self.assertEqual("b", result[0][1].literal_value)
        self.assertEqual("a", result[1][0].literal_value)
        self.assertEqual("b", result[1][1].literal_value)
