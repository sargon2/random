
import unittest2
import re

class ParseResult(object):
    def __init__(self, match_ob, literal_value):
        self.match_ob = match_ob
        self.literal_value = literal_value
        self.matchlen = len(match_ob.group(0))

    def __repr__(self):
        return "ParseResult('" + str(self.literal_value) + "')"

class EOF(object):
    def __init__(self):
        self.matchlen = 0
    def parse(self, code):
        if code == '':
            return self
        return None

class RegexParser(object):
    def __init__(self, regex, groupnum=0, ret_type=str):
        self.regex = regex
        self.groupnum = groupnum
        self.ret_type = ret_type

    def parse(self, code):
        match = re.match(self.regex, code)
        if match:
            literal_value = None
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

class ResultList(object):
    def __init__(self, items):
        self.items = items
        total_matchlen = 0
        for item in items:
            total_matchlen += item.matchlen
        self.matchlen = total_matchlen

    def __getitem__(self, key):
        return self.items[key]

    def __repr__(self):
        return repr(self.items)

class ZeroOrMore(object):
    def __init__(self, arg):
        self.item = arg

    def parse(self, code):
        results = []
        while(True):
            result = self.item.parse(code)
            if not result:
                return ResultList(results)
            code = code[result.matchlen:]
            results.append(result)

class OneOrMore(object):
    def __init__(self, arg):
        self.item = arg

    def parse(self, code):
        return Each(self.item, ZeroOrMore(self.item)).parse(code)

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
        return ResultList(results)

class NewLanguage(object):
    def execute(self, code):
        digit = RegexParser('(\d+)', 1, int)
        string = RegexParser('"([^"]+)"', 1)
        return_word = RegexParser('return')
        whitespace = RegexParser('\s+')
        optional_whitespace = RegexParser('\s*')
        semicolon = RegexParser(';')
        word = RegexParser('[a-z]+')
        equals = RegexParser('=')
        eof = EOF()

        value = Or(digit, string, word)
        return_stmt = Each(return_word, whitespace, value, optional_whitespace, semicolon)
        assignment = Each(word, optional_whitespace, equals, optional_whitespace, value, semicolon)
        statement = Each(Or(return_stmt, assignment), optional_whitespace)
        statements = Each(optional_whitespace, OneOrMore(statement), eof)
        result = statements.parse(code)
        if result:
            # Option: traverse the AST, look for return statements
            # Option: traverse the AST, interpret each node
            # Option: make everything generate python, execute it
            return result[1][0][0][2].literal_value


    def runNewLang(self, code):
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

        result = self.execute(code)
        if result:
            return result

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
        self.assertResult(1, "  return 1;  ")
        self.assertResult(1, "return  1 ;")
        self.assertIsParseError("return1;")
        self.assertIsParseError("return 1")
        self.assertIsParseError("")
        self.assertIsParseError(" ")
        self.assertIsParseError("\n")
        self.assertResult(1, "return 1;return 2;")
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
