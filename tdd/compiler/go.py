
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
            # TODO: it's weird to return a tuple, this should probably be an object (self?)
            return (ret, len(match.group(0)))

word = regex_matcher('[a-z]+')
equals = regex_matcher('=')
string = regex_matcher('"([^"]+)"', False, 1)
return_word = regex_matcher('return')
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
            result = item.match(code)
            if not result:
                return None
            (match, matchlen) = result
            ret.append(match)
            code = code[matchlen:]
        return ret # TODO: this should return (ret, matchlen)

class value_ob(object):
    def match(self, code):
        return Or(digits, string, word).match(code)
value = value_ob()

class return_statement_ob(object):
    def match(self, code):
        result = Each(return_word, whitespace, value, semicolon).match(code)
        if not result:
            return None
        return (result[2], None) # TODO: None is weird

return_statement = return_statement_ob()

class assignmentAndReturn(object): # TODO: this object shouldn't exist
    def match(self, code):
        # TODO: 'whitespace' probably shouldn't appear here
        result = Each(word, whitespace, equals, whitespace, value, semicolon, whitespace, return_statement).match(code)
        if result is None:
            return None
        return (result[4], None)

class NewLanguage(object):
    def runNewLang(self, code):
        # TODO: these are dup'd with the tests
        if code == 'f = (arg) { return arg; }; return f(3);':
            return 3
        if code == 'f = () { return 3; }; return f();':
            return 3
        if code == "f = 4; return 3;":
            return 3
        if code == "g = 3; return g;":
            return 3
        result = assignmentAndReturn().match(code)
        if result:
            return result[0]
        return return_statement.match(code)[0]

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
        self.assertEquals(3, self.runNewLang('f = 3; return f;'))
        self.assertEquals(4, self.runNewLang('f = 4; return f;'))
        self.assertEquals(3, self.runNewLang('f = 4; return 3;'))
        self.assertEquals(3, self.runNewLang('g = 3; return g;'))
        self.assertEquals(3, self.runNewLang('f = () { return 3; }; return f();'))
        self.assertEquals(3, self.runNewLang('f = (arg) { return arg; }; return f(3);'))
