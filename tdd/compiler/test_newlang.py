
import unittest2
import newlang
import subprocess

class TestNewLanguage(unittest2.TestCase):
    def runNewLang(self, code):
        a = newlang.NewLanguage()
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
        self.assertResult(3, 'f = (arg1, arg2) { return arg1; }; return f(3, 4);')
        self.assertResult(4, 'f = (arg1, arg2) { return arg2; }; return f(3, 4);')
        self.assertResult(3, ' f = ( arg1 , arg2 ) { return arg1 ; } ; return f ( 3 , 4 ) ; ')
        self.assertResult(3, 'f=(arg1,arg2){return arg1;};return f(3,4);')
        self.assertResult('3\n', 'a=`echo 3`;return a;')
        self.assertResult('3\n', 'a = ` echo 3 ; ` ; return a ;')
        self.assertResult(3, 'f = (arg1) { return arg1; }; g = (arg1) { return arg1; }; return (f(1) + g(2));')
        self.assertResult(3, 'f = (arg1) { return arg1; }; f(4); return 3;')
        self.assertResult("text from file", 'a = "text from file"; write_file("delme.txt", a); return read_file("delme.txt");')
        self.assertResult("3\n", 'a = 3; return `echo {a}`;')
        self.assertResult("catted str", 'a = "catted str"; return `cat`(a);')
        self.assertResult(3, "# comment\nreturn 3; # comment")
        # TODO: if
        # self.assertResult(3, "if(equals(1, 2), { return 2; }); return 3;)")
        # self.assertResult(2, "if(equals(1, 1), { return 2; }); return 3;)")

        # TODO: for
        # TODO: backticks as a statement
        # TODO: return code from backticks
        # TODO: comments
        # TODO: prints
        # TODO: in compiler-source.newlang, print the output of gcc instead of eating it

    @unittest2.skip("not passing yet")
    def test_bootstrap(self):
        # Bootstrap compile:
        try:
            print subprocess.check_output(["./bootstrap-compile", "-o", "compile", "compiler-source.newlang"])
        except Exception as e:
            print "Output:"
            print e.output
            raise

        # Get rid of all traces of the bootstrap compiler:
        print subprocess.check_output(["./compile", "-o", "compile", "compiler-source.newlang"])

        # Verify:
        print subprocess.check_output(["./compile", "-o", "verify", "compiler-source.newlang"])
        print subprocess.check_output(["diff", "compile", "verify"])
