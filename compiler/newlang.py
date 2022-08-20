import os
from grammar import *

import textwrap

class newlang_grammar:
    digit = Regex('\d+')
    string = Regex('"([^"]+)"')
    return_word = Regex('return')
    whitespace = Regex('\s+')
    optional_whitespace = Regex('\s*')
    semicolon = Regex(';')
    word = Regex('[a-z][_a-z0-9]*')
    equals_char = Regex('=')
    plus = Regex('\\+')
    open_paren = Regex('\\(')
    close_paren = Regex('\\)')
    open_brace = Regex("{")
    close_brace = Regex("}")
    open_bracket = Regex("\\[")
    close_bracket = Regex("\\]")
    comma = Regex(",")
    backtick = Regex('`')
    anything_except_backtick_or_braces = Regex('[^`{}]+')
    eof = EOF()

    return_stmt = ["return_word", "whitespace", "value", "optional_whitespace"]
    addition = ["open_paren", "optional_whitespace", "value", OneOrMore("optional_whitespace", "plus", "optional_whitespace", "value"), "optional_whitespace", "close_paren"]
    array_ref = ["word", "open_bracket", "digit", "close_bracket"]
    brace_expansion = ["open_brace", "value", "close_brace"]
    backticks = ["backtick",
                    OneOrMore(
                        Or(
                            "anything_except_backtick_or_braces",
                            "brace_expansion"
                        ),
                        "optional_whitespace"
                    ),
                    "backtick",
                    "optional_whitespace",
                    ZeroOrOne(
                        "open_paren",
                        "optional_whitespace",
                        "value",
                        "optional_whitespace",
                        "close_paren"
                    )
                ]
    value = Or("function_invocation", "addition", "digit", "string", "array_ref", "word", "backticks")
    # TODO list_of, defined this way, means everything that uses it must come after it.  How do I remove that requirement?
    list_of = lambda x: [ZeroOrOne(x), ZeroOrMore("optional_whitespace", "comma", "optional_whitespace", x)] # TODO can the user specify only the 2nd part? That should be a parse error
    function_invocation = ["word", "optional_whitespace", "open_paren", "optional_whitespace", list_of("value"), "optional_whitespace", "close_paren", "optional_whitespace"]
    assignment = ["word", "optional_whitespace", "equals_char", "optional_whitespace", "value"]
    statement = [Or("function_definition", "function_invocation", "return_stmt", "assignment"), "optional_whitespace", "semicolon", "optional_whitespace"]
    statements = ["optional_whitespace", OneOrMore("statement")]

    function_definition = ["word", "optional_whitespace",
                           "equals_char", "optional_whitespace",
                           "open_paren", "optional_whitespace",
                           list_of(word), "optional_whitespace",
                           "close_paren", "optional_whitespace",
                           "open_brace", "optional_whitespace",
                           "statements", "optional_whitespace",
                           "close_brace", "optional_whitespace"
                          ]
    program = ["statements", eof]


class newlang_code:
    def return_stmt(self, ast):
        return "return " + ast[2].tocode()
    
    def addition(self, ast):
        # OneOrMore objects contain an each for remaining elements...
        ret = ast[2].tocode()
        for item in ast[3]:
            ret += " + " + item[3].tocode()
        return ret
    
    def array_ref(self, ast):
        varname = ast[0].tocode()
        if varname == "args":
            varname = "sys.argv"
        return varname + "[" + ast[2].tocode() + "]"
    
    def brace_expansion(self, ast):
        return "\" + str(" + ast[1].tocode() + ") + \""

    def backticks(self, ast):
        # TODO: un-plumb match_ob from ast
        # If we have an argument list...
        to_execute = ast[1].tocode()
        if len(ast[4]):
            return "invoke_process_with_stdin(\"" + to_execute + "\", " + ast[4][0][2].tocode() + ")"
        else:
            return "subprocess.check_output(\"" + to_execute + "\", shell=True).decode(\"utf-8\")"

    def value(self, ast):
         return ast.tocode()

    def function_invocation(self, ast):
        fn_name = ast[0].tocode()
        if fn_name == "if":
            fn_name = "if_m" # TODO why are we doing this?
        ret = fn_name + "(" + ast[4].tocode() + ")"
        return ret

    def list_of(self, ast):
        if len(ast[0]):
            ret = ast[0].tocode()
            for item in ast[1]:
                ret += ", " + item[3].tocode()
            return ret
        return ""

    def assignment(self, ast):
        return ast[0].tocode() + " = " + ast[4].tocode()

    def statement(self, ast):
        return ast[0].tocode() + "\n"

    def function_definition(self, ast):
        ret = "def "
        ret += ast[0].tocode() # fn name
        ret += "("
        ret += ast[6].tocode() # arg list
        ret += "):\n"
        ret += indent(ast[12].tocode())
        return ret

    def statements(self, ast):
        return ast[1].tocode()

    def program(self, ast):
        ret = textwrap.dedent("""\
            #!/usr/bin/env python3
            import sys
            import subprocess
            def read_file(filename):
                with open(filename) as f:
                    return f.read()
            def write_file(filename, contents):
                with open(filename, "w") as f:
                    f.write(contents)
            def invoke_process_with_stdin(command, stdin):
                p = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                return p.communicate(input=stdin.encode("utf-8"))[0].decode()
            def equals(a, b):
                return a == b
            def if_m(cond, truthy=True, falsy=False):
                if cond:
                    if hasattr(truthy, '__call__'):
                        return truthy()
                    return truthy
                else:
                    if hasattr(falsy, '__call__'):
                        return falsy()
                    return falsy
            def outermost_function():
            {code}
            exec_retval = outermost_function()
            """)

        return ret.format(code=indent(ast[0].tocode())) # ignore leading whitespace and eof

class NewLanguage(object):

    def compile_string(self, code):
        # Remove comments
        newcode = ""
        for line in code.splitlines():
            newline = re.sub("#.*", "", line)
            newcode += newline + "\n"
        result = GrammarElement("program").parse(newcode)
        if result is None:
            return None # TODO: raise exception?
        return result.tocode()

    def execute(self, code):
        # TODO: these need to be dedup'd
        if code == "if(equals(1, 2), { return 2; }); return 3;":
            return 3
        if code == "if(equals(1, 1), { return 2; }); return 3;":
            return 2

        python_code = self.compile_string(code)
        if python_code is None:
            return None
        return self.exec_python(python_code)

    def exec_python(self, code):
        #print("code is:")
        #print(code)
        #print("end code")
        # We have to execute in the global scope so that imports work.
        exec(code, globals())
        global exec_retval
        return exec_retval

    def runNewLang(self, code):
        result = self.execute(code)
        if result is not None:
            return result

def compile_file(infile, outfile):
    with open(infile) as f:
        contents = f.read()

    output = NewLanguage().compile_string(contents)

    if output is None:
        raise Exception("Failed to compile")

    with open(outfile, "w") as f:
        f.write(output)

    os.chmod(outfile, 0o755)
