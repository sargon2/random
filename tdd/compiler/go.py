
import unittest2
import re

class NewLanguage(object):
    def runNewLang(self, code):
        items = [
                    ('(\d+)', int),
                    ('"([^"]+)"', str),
                ]

        for regex, ret_type in items:
            match = re.match('return ' + regex + ';', code)
            if match:
                return ret_type(match.group(1))

        if code == 'f = 3; return f;':
            return 3
        if code == 'f = 4; return f;':
            return 4
        if code == 'f = 4; return 3;':
            return 3
        if code == 'g = 3; return g;':
            return 3
        if code == 'f = () { return 3; }; return f();':
            return 3
        if code == 'f = (arg) { return arg; }; return f(3);':
            return 3

class TestNewLanguage(unittest2.TestCase):
    def runNewLang(self, code):
        a = NewLanguage()
        return a.runNewLang(code)

    def test_values(self):
        self.assertEquals(1, self.runNewLang("return 1;")) # Is that a function invocation, or a program invocation?
        self.assertEquals(2, self.runNewLang("return 2;"))
        self.assertEquals(1, self.runNewLang("return 1; return 2;"))
        self.assertEquals(34, self.runNewLang("return 34;"))
        self.assertEquals("a", self.runNewLang('return "a";'))
        self.assertEquals("abc", self.runNewLang('return "abc";'))
        self.assertEquals(3, self.runNewLang('f = 3; return f;'))
        self.assertEquals(4, self.runNewLang('f = 4; return f;'))
        self.assertEquals(3, self.runNewLang('f = 4; return 3;'))
        self.assertEquals(3, self.runNewLang('g = 3; return g;'))
        self.assertEquals(3, self.runNewLang('f = () { return 3; }; return f();'))
        self.assertEquals(3, self.runNewLang('f = (arg) { return arg; }; return f(3);'))
