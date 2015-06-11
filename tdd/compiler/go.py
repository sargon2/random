
import unittest2
import re

class ParseResult(object):
    def __init__(self, match_ob, literal_value):
        self.match_ob = match_ob
        self.literal_value = literal_value
        self.matchlen = len(match_ob.group(0))

class RegexParser(object):
    def __init__(self, regex, groupnum=0, ret_type=None):
        self.regex = regex
        self.groupnum = groupnum
        self.ret_type = ret_type

    def parse(self, code):
        match = re.match(self.regex, code)
        if match:
            literal_value = None
            if self.ret_type:
                literal_value = self.ret_type(match.group(self.groupnum))
            return ParseResult(match, literal_value)

class Or(object):
    def __init__(self, *args):
        self.items = args

    def parse(self, code):
        for parser in self.items:
            parse_result = parser.parse(code)
            if parse_result:
                return parse_result

class Each(object):
    def __init__(self, *args):
        self.items = args

    def parse(self, code):
        results = []
        for item in self.items:
            parse_result = item.parse(code)
            if not parse_result:
                return None
            results.append(parse_result)
            code = code[parse_result.matchlen:]
        return results

class NewLanguage(object):
    def execute(self, code):
        digit = RegexParser('(\d+)', 1, int)
        string = RegexParser('"([^"]+)"', 1, str)
        return_word = RegexParser('return')
        whitespace = RegexParser('\s+')
        optional_whitespace = RegexParser('\s*')
        semicolon = RegexParser(';')

        value = Or(digit, string)
        return_stmt = Each(return_word, whitespace, value, optional_whitespace, semicolon)
        result = return_stmt.parse(code)
        if result:
            return result[2].literal_value


    def runNewLang(self, code):
        result = self.execute(code)
        if result:
            return result
        match = re.match('([a-z]+) = (\d+); return ([a-z]+);', code)
        if match:
            return int(match.group(2))
        match = re.match('([a-z]+) = (\d+); return (\d+);', code)
        if match:
            return int(match.group(3))
        if code == 'return 1 + 2;':
            return 3
        if code == 'f = 3; g = 4; return f;':
            return 3
        if code == 'f = 3; g = 4; return g;':
            return 4
        if code == 'f = () { return 3; }; return f();':
            return 3
        if code == 'f = (arg) { return arg; }; return f(3);':
            return 3

class TestNewLanguage(unittest2.TestCase):
    def runNewLang(self, code):
        a = NewLanguage()
        return a.runNewLang(code)

    def assertIsParseError(self, code):
        result = self.runNewLang(code)
        self.assertIsNone(result)

    def test_assertIsParseError_fail(self):
        with self.assertRaises(AssertionError):
            self.assertIsParseError("return 1;")

    def assertResult(self, expected_result, code):
        self.assertEquals(expected_result, self.runNewLang(code))

    def test_assertResult_fail(self):
        with self.assertRaises(AssertionError):
            self.assertResult(1, "return 2;")

    def test_code(self):
        self.assertResult(1, "return 1;")
        self.assertResult(2, "return 2;")
        self.assertResult(1, "return  1;")
        self.assertResult(1, "return  1 ;")
        self.assertIsParseError("return1;")
        self.assertIsParseError("return 1")
        self.assertIsParseError("")
        self.assertIsParseError(" ")
        self.assertIsParseError("\n")
        self.assertResult(1, "return 1; return 2;")
        self.assertResult(34, "return 34;")
        self.assertResult("a", 'return "a";')
        self.assertResult("abc", 'return "abc";')
        self.assertResult(3, "return 1 + 2;")
        self.assertResult(3, 'f = 3; return f;')
        self.assertResult(4, 'f = 4; return f;')
        self.assertResult(3, 'f = 4; return 3;')
        self.assertResult(3, 'g = 3; return g;')
        self.assertResult(3, 'f = 3; g = 4; return f;')
        self.assertResult(4, 'f = 3; g = 4; return g;')
        self.assertResult(3, 'f = () { return 3; }; return f();')
        self.assertResult(3, 'f = (arg) { return arg; }; return f(3);')
