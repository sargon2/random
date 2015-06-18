
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
            #print code
            #print "matched", self.regex
            literal_value = None
            literal_value = self.ret_type(match.group(self.groupnum))
            return ParseResult(match, literal_value)

class Or(object):
    def __init__(self, *args):
        self.items = args

    def parse(self, code):
        for parser in self.items:
            parse_result = parser.parse(code)
            if parse_result is not None:
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

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return "ResultList(" + repr(self.items) + ")"

class ZeroOrMore(object):
    def __init__(self, arg):
        self.item = arg

    def parse(self, code):
        results = []
        while(True):
            result = self.item.parse(code)
            if result is None:
                return ResultList(results)
            code = code[result.matchlen:]
            results.append(result)

class OneOrMore(object):
    def __init__(self, arg):
        self.item = arg

    def parse(self, code):
        return Each(self.item, ZeroOrMore(self.item)).parse(code)

class ZeroOrOne(object):
    def __init__(self, arg):
        self.item = arg

    def parse(self, code):
        result = self.item.parse(code)
        if result is None:
            return ResultList([])
        return ResultList([result])

class Each(object):
    def __init__(self, *args):
        self.items = args

    def parse(self, code):
        results = []
        for item in self.items:
            parse_result = item.parse(code)
            if parse_result is None:
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

class string_ob(object):
    def defn(self):
        return RegexParser('"([^"]+)"', 1)

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
plus = RegexParser('\\+')
open_paren = RegexParser('\\(')
close_paren = RegexParser('\\)')
open_brace = RegexParser("{")
close_brace = RegexParser("}")
comma = RegexParser(",")
eof = EOF()

class return_stmt_ob(object):
    def defn(self):
        return Each(return_word, whitespace, value, optional_whitespace)

    def tocode(self, ast):
        return "return " + str(ast[2].tocode()) + "\n"
        return return_stmt_result(result)

return_stmt = GrammarElement(return_stmt_ob)

class addition_ob(object):
    def defn(self):
        remaining_plus = Each(optional_whitespace, plus, optional_whitespace, value)
        return Each(open_paren, optional_whitespace, value, OneOrMore(remaining_plus), optional_whitespace, close_paren)

    def tocode(self, ast):
        # OneOrMore objects contain an each for remaining elements...
        ret = str(ast[2].tocode()) + " + " + str(ast[3][0][3].tocode())
        for item in ast[3][1]:
            ret += " + " + str(item[3].tocode())
        return ret

addition = GrammarElement(addition_ob)

class value_ob(object):
    def defn(self):
        return Or(function_invocation, addition, digit, string, word)

    def tocode(self, ast):
        return ast.tocode()

value = GrammarElement(value_ob)

class assignment_ob(object):
    def defn(self):
        return Each(word, optional_whitespace, equals, optional_whitespace, value)

    def tocode(self, ast):
        return ast[0].tocode() + " = " + str(ast[4].tocode()) + '\n'

assignment = GrammarElement(assignment_ob)

class statement_ob(object):
    def defn(self):
        return Each(Or(function_definition, return_stmt, assignment), optional_whitespace, semicolon, optional_whitespace)

    def tocode(self, ast):
        return ast[0].tocode()

statement = GrammarElement(statement_ob)

class list_of_ob(object):
    def __init__(self, item):
        self.item = item

    def defn(self):
        return Each(ZeroOrOne(self.item), ZeroOrMore(Each(comma, self.item)))

    def tocode(self, ast):
        if len(ast[0]):
            ret = ast[0].tocode()
            # TODO: rest of items
            return ret
        return ""

def list_of(value):
    return GrammarElement(lambda: list_of_ob(value))

class function_definition_ob(object):
    def defn(self):
        return Each(
                word, optional_whitespace,
                equals, optional_whitespace,
                open_paren, optional_whitespace,
                list_of(word), optional_whitespace,
                close_paren, optional_whitespace,
                open_brace, optional_whitespace,
                statements, optional_whitespace,
                close_brace, optional_whitespace)

    def tocode(self, ast):
        ret = "def "
        ret += ast[0].tocode() # fn name
        ret += "("
        ret += ast[6].tocode() # arg list
        ret += "):\n"
        ret += indent(ast[12].tocode()) # statements
        return ret

function_definition = GrammarElement(function_definition_ob)

class function_invocation_ob(object):
    def defn(self):
        return Each(word, open_paren, optional_whitespace, list_of(value), optional_whitespace, close_paren, optional_whitespace)

    def tocode(self, ast):
        ret = ast[0].tocode() + "(" + ast[3].tocode() + ")"
        return ret

function_invocation = GrammarElement(function_invocation_ob)

class statements_ob(object):
    def defn(self):
        return Each(optional_whitespace, OneOrMore(statement))

    def tocode(self, ast):
        return ast[1].tocode()

statements = GrammarElement(statements_ob)

class program_ob(object):
    def defn(self):
        return Each(statements, eof)

    def tocode(self, ast):
        ret = "def outermost_function():\n"
        ret += indent(ast[0].tocode()) # ignore leading whitespace and eof
        ret += "exec_retval = outermost_function()"
        return ret

program = GrammarElement(program_ob)

class NewLanguage(object):
    def execute(self, code):

        result = program.parse(code)
        if result is not None:
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
        result = self.execute(code)
        if result is not None:
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
        self.assertIsParseError("return 1 + 2;") # TODO: how to make this work without stack overflow?
        self.assertResult(3, "return (1+2);")
        self.assertResult(6, "return ((1+2)+3);")
        self.assertResult(6, "return (1+(2+3));")
        self.assertResult(6, "return (1+2+3);")
        self.assertResult(6, " return ( 1 + 2 + 3 ) ; ")
        self.assertResult(3, " return ( 1 + 2 ) ; ")
        self.assertResult(3, "a = 1; return (a + 2);")
        self.assertResult(3, "a = 1; return (2 + a);")
        self.assertResult(3, "a = 1; b = 2; return (a + b);")
        self.assertResult(3, 'f = 3; return f;')
        self.assertResult(4, 'f = 4; return f;')
        self.assertResult(3, 'f = 4; return 3;')
        self.assertResult(3, 'g = 3; return g;')
        self.assertResult(3, 'f = 3; g = 4; return f;')
        self.assertResult(4, 'f = 3; g = 4; return g;')
        self.assertResult(3, 'f = () { return 3; }; return f();')
        self.assertResult(3, 'f = (arg) { return arg; }; return f(3);')
        #self.assertResult(3, 'f = (arg1, arg2) { return arg1; }; return f(3, 4);')
        #self.assertResult(4, 'f = (arg1, arg2) { return arg2; }; return f(3, 4);')
