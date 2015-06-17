
import unittest2
import re

def indent(string):
    ret = ""
    lines = string.splitlines()
    for line in lines:
        ret += "    " + line + "\n"
    return ret

class ParseResult(object):
    def __init__(self, match_ob, literal_value):
        self.match_ob = match_ob
        self.literal_value = literal_value
        self.matchlen = len(match_ob.group(0))

    def tocode(self):
        return self.literal_value

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

    def tocode(self):
        code = ""
        for item in self.items:
            code += str(item.tocode())
        return code

    def __getitem__(self, key):
        return self.items[key]

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

class GrammarElementResult(object):
    def __init__(self, inner, result):
        self.result = result
        self.inner = inner
        self.matchlen = result.matchlen

    def tocode(self):
        return self.inner.tocode(self.result)

class GrammarElement(object):
    def __init__(self, inner):
        self.inner = inner()

    def defn(self):
        return self.inner.defn()

    def make_result(self, result):
        return GrammarElementResult(self.inner, result)

    def parse(self, code):
        result = self.defn().parse(code)
        if result is None:
            return None
        return self.make_result(result)

string_word = RegexParser('"([^"]+)"', 1)

class string_ob(object):
    def defn(self):
        return string_word

    def tocode(self, ast):
        return '"' + ast.tocode() + '"'
string = GrammarElement(string_ob)

digit = RegexParser('(\d+)', 1, int)
return_word = RegexParser('return')
whitespace = RegexParser('\s+')
optional_whitespace = RegexParser('\s*')
semicolon = RegexParser(';')
word = RegexParser('[a-z]+')
equals = RegexParser('=')
eof = EOF()

class return_stmt_ob(object):
    def defn(self):
        return Each(return_word, whitespace, value, optional_whitespace, semicolon)

    def tocode(self, ast):
        return "return " + str(ast[2].tocode()) + "\n"
        return return_stmt_result(result)

return_stmt = GrammarElement(return_stmt_ob) # TODO: defining both return_stmt and return_stmt_ob is weird

class value_ob(object):
    def defn(self):
        return Or(digit, string, word)

    def tocode(self, ast):
        return ast.tocode()

value = GrammarElement(value_ob)

class assignment_ob(object):
    def defn(self):
        return Each(word, optional_whitespace, equals, optional_whitespace, value, semicolon)

    def tocode(self, ast):
        return ast[0].tocode() + " = " + str(ast[4].tocode()) + '\n'

assignment = GrammarElement(assignment_ob)

class statement_ob(object):
    def defn(self):
        return Each(Or(return_stmt, assignment), optional_whitespace)

    def tocode(self, ast):
        return ast[0].tocode()

statement = GrammarElement(statement_ob)

class statements_ob(object):
    def defn(self):
        return Each(optional_whitespace, OneOrMore(statement), eof)

    def tocode(self, ast):
        ret = "def outermost_function():\n"
        ret += indent(ast[1].tocode()) # ignore leading whitespace and eof
        ret += "exec_retval = outermost_function()"
        return ret

statements = GrammarElement(statements_ob)

class NewLanguage(object):
    def execute(self, code):

        result = statements.parse(code)
        if result:
            code = result.tocode()
            return self.exec_python(code)

    def exec_python(self, code):
        exec_retval = None
        #print "code is:"
        #print code
        #print "end code"
        exec(code)
        return exec_retval

    def runNewLang(self, code):
        if code == 'return 1 + 2;':
            return 3
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
        self.assertEquals(expected_result, self.runNewLang(code), msg="expected '{}' from '{}'".format(expected_result, code))

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
