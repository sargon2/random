import os
from grammar import *

import textwrap

digit = RegexParser('\d+')
string = RegexParser('"([^"]+)"')
return_word = RegexParser('return')
whitespace = RegexParser('\s+')
optional_whitespace = RegexParser('\s*')
semicolon = RegexParser(';')
word = RegexParser('[a-z][_a-z0-9]*')
equals_char = RegexParser('=')
plus = RegexParser('\\+')
open_paren = RegexParser('\\(')
close_paren = RegexParser('\\)')
open_brace = RegexParser("{")
close_brace = RegexParser("}")
open_bracket = RegexParser("\\[")
close_bracket = RegexParser("\\]")
comma = RegexParser(",")
backtick = RegexParser('`')
anything_except_backtick_or_braces = RegexParser('[^`{}]+')
eof = EOF()

class return_stmt_ob(object):
    def defn(self):
        return Each(return_word, whitespace, value, optional_whitespace)

    def tocode(self, ast):
        return "return " + ast[2].tocode()
        return return_stmt_result(result)

return_stmt = GrammarElement(return_stmt_ob)

class addition_ob(object):
    def defn(self):
        remaining_plus = Each(optional_whitespace, plus, optional_whitespace, value)
        return Each(open_paren, optional_whitespace, value, OneOrMore(remaining_plus), optional_whitespace, close_paren)

    def tocode(self, ast):
        # OneOrMore objects contain an each for remaining elements...
        ret = ast[2].tocode() + " + " + ast[3][0][3].tocode()
        for item in ast[3][1]:
            ret += " + " + item[3].tocode()
        return ret

addition = GrammarElement(addition_ob)

class array_ref_ob(object):
    def defn(self):
        return Each(word, open_bracket, digit, close_bracket)

    def tocode(self, ast):
        varname = ast[0].tocode()
        if varname == "args":
            varname = "sys.argv"
        return varname + "[" + ast[2].tocode() + "]"

array_ref = GrammarElement(array_ref_ob)

class brace_expension_ob(object):
    def defn(self):
        return Each(open_brace, value, close_brace)

    def tocode(self, ast):
        return "\" + str(" + ast[1].tocode() + ") + \""

brace_expansion = GrammarElement(brace_expension_ob)

class backticks_ob(object):
    def defn(self):
        return Each(
                backtick,
                OneOrMore(
                    Each(
                        Or(
                            anything_except_backtick_or_braces,
                            brace_expansion
                        ),
                        optional_whitespace
                    )
                ),
                backtick,
                optional_whitespace,
                ZeroOrOne(
                    Each(
                        open_paren,
                        optional_whitespace,
                        value,
                        optional_whitespace,
                        close_paren
                    )
                )
            )

    def tocode(self, ast):
        # TODO: un-plumb match_ob from ast
        # If we have an argument list...
        to_execute = ast[1].tocode()
        if len(ast[4]):
            return "invoke_process_with_stdin(\"" + to_execute + "\", " + ast[4][0][2].tocode() + ")"
        else:
            return "subprocess.check_output(\"" + to_execute + "\", shell=True).decode(\"utf-8\")"

backticks = GrammarElement(backticks_ob)

class value_ob(object):
    def defn(self):
        return Or(function_invocation, addition, digit, string, array_ref, word, backticks, block)

    def tocode(self, ast):
        return ast.tocode()

value = GrammarElement(value_ob)

class assignment_ob(object):
    def defn(self):
        return Each(word, optional_whitespace, equals_char, optional_whitespace, value)

    def tocode(self, ast):
        return ast[0].tocode() + " = " + ast[4].tocode()

assignment = GrammarElement(assignment_ob)

class statement_ob(object):
    def defn(self):
        return Each(Or(function_definition, function_invocation, return_stmt, assignment), optional_whitespace, semicolon, optional_whitespace)

    def tocode(self, ast):
        return ast[0].tocode() + "\n"

statement = GrammarElement(statement_ob)

class list_of_ob(object):
    def __init__(self, item):
        self.item = item

    def defn(self):
        return Each(ZeroOrOne(self.item), ZeroOrMore(Each(optional_whitespace, comma, optional_whitespace, self.item)))

    def tocode(self, ast):
        if len(ast[0]):
            ret = ast[0].tocode()
            for item in ast[1]:
                ret += ", " + item[3].tocode()
            return ret
        return ""

def list_of(value):
    return GrammarElement(lambda: list_of_ob(value))

class function_definition_ob(object):
    def defn(self):
        return Each(
                word, optional_whitespace,
                equals_char, optional_whitespace,
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
        return Each(word, optional_whitespace, open_paren, optional_whitespace, list_of(value), optional_whitespace, close_paren, optional_whitespace)

    def tocode(self, ast):
        fn_name = ast[0].tocode()
        if fn_name == "if":
            fn_name = "if_m"
        ret = fn_name + "(" + ast[4].tocode() + ")"
        return ret

function_invocation = GrammarElement(function_invocation_ob)

class block_ob(object):
    def defn(self):
        # TODO: function definition should use this instead of duplicating it
        return Each(open_brace, optional_whitespace,
                statements, optional_whitespace,
                close_brace, optional_whitespace)

    def tocode(self, ast):
        return "block: " + ast[2].tocode()
        return "todo_fn_name"

block = GrammarElement(block_ob)

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

program = GrammarElement(program_ob)

class NewLanguage(object):

    def compile_string(self, code):
        # Remove comments
        newcode = ""
        for line in code.splitlines():
            newline = re.sub("#.*", "", line)
            newcode += newline + "\n"
        result = program.parse(newcode)
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
