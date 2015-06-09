
import unittest2
import re

class regex_matcher(object):
    def __init__(self, regex, intify=False, groupnum=0):
        self.regex = regex
        self.groupnum = groupnum
        self.intify = intify

    def match(self, code):
        match = re.match(self.regex, code)
        if match:
            ret = match.group(self.groupnum)
            if self.intify:
                ret = int(ret)
            return (ret, len(match.group(0)))

string = regex_matcher('"([^"]+)"', False, 1)
return_ob = regex_matcher('return')
whitespace = regex_matcher('\s+')
semicolon = regex_matcher(';')
digits = regex_matcher("[0-9]+", True)

class Or(object):
    def __init__(self, *args):
        self.items = args

    def match(self, code):
        for item in self.items:
            result = item.match(code)
            if result:
                return result

class Each(object):
    def __init__(self, *args):
        self.items = args

    def match(self, code):
        ret = []
        for item in self.items:
            (match, matchlen) = item.match(code)
            if not match:
                return None
            ret.append(match)
            code = code[matchlen:]
        return ret

class return_statement_ob(object):
    def match(self, code):
        return Each(return_ob, whitespace, Or(digits, string), semicolon).match(code)[2]

return_statement = return_statement_ob()

class NewLanguage(object):
    def runNewLang(self, code):
        return return_statement.match(code)

class TestNewLanguage(unittest2.TestCase):
    def runNewLang(self, code):
        a = NewLanguage()
        return a.runNewLang(code)

    def test_values(self):
        self.assertEquals(1, self.runNewLang("return 1;")) # Is that a function invocation, or a program invocation?
        self.assertEquals(2, self.runNewLang("return 2;"))
        self.assertEquals(34, self.runNewLang("return 34;"))
        self.assertEquals("a", self.runNewLang('return "a";'))
        self.assertEquals("abc", self.runNewLang('return "abc";'))
        # self.assertEquals(3, self.runNewLang('f = 3; return f;'))
        # self.assertEquals(4, self.runNewLang('f = 4; return f;'))
        # self.assertEquals(3, self.runNewLang('g = 3; return g;'))
        # self.assertEquals(3, self.runNewLang('f = () { return 3; }; return f();'))
        # self.assertEquals(3, self.runNewLang('f = (arg) { return arg; }; return f(3);'))
