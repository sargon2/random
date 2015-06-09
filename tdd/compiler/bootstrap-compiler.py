#!/usr/bin/env python

import sys
import os
import re

outfile = sys.argv[2]
infile = sys.argv[3]

with open(infile) as f:
    contents = f.read()

# TODO: globals are bad, make a class so they can be instance variables instead

# TODO: all the lambdas are weird.  It would be better to have item_ob and item = item_ob() at least (i.e. remove the instantiation call from parse())
# TODO: pass the code around instead of making it global -- should remove the need for backtrack
# TODO: keep track of position and matchlen instead of using re.findall() (re.findall() dups the re checks)

class SingleToken(object):
    def __init__(self, result):
        self.result = result
    def tocode(self):
        return self.result
    def __repr__(self):
        return self.result

token = None
def try_consume(regex):
    global position
    global token
    if position >= len(tokens):
        return None
    token = tokens[position]
    if re.match(regex, token):
        position += 1
        return SingleToken(token)
    return None

def is_bad_parse(result):
    if result is None:
        return True
    if isinstance(result, list):
        return False
    if result.result is None:
        return True

def backtrack(fn):
    def wrapper(*args, **kwargs):
        global position
        orig_position = position
        result = fn(*args, **kwargs)
        if is_bad_parse(result):
            position = orig_position
        return result
    return wrapper

def Or(*args):
    return lambda: Or_ob(*args)

class Or_ob(object):
    def __init__(self, *args):
        self.args = args

    @backtrack
    def parse(self):
        for item in self.args:
            if isinstance(item, str):
                item = literal(item)
            r = parse(item)
            if not is_bad_parse(r):
                self.result = r
                return r
        return None

def Each(*args):
    return lambda: Each_ob(*args)
class Each_ob(object):
    def __init__(self, *args):
        self.args = args

    @backtrack
    def parse(self):
        ret = []
        for item in self.args:
            if isinstance(item, str):
                item = literal(item)
            r = parse(item)
            if is_bad_parse(r):
                return r
            ret.append(r)

        self.result = ret
        return ret

def ZeroOrOne(*args):
    return lambda: ZeroOrOne_ob(*args)
class ZeroOrOne_ob(object):
    def __init__(self, arg):
        self.arg = arg

    def parse(self):
        r = parse(self.arg)
        if is_bad_parse(r):
            self.result = []
            return []
        self.result = r
        return r

def ZeroOrMore(*args):
    return lambda: ZeroOrMore_ob(*args)

class ZeroOrMore_ob(object):

    def __init__(self, arg):
        self.arg = arg

    def parse(self):
        done = False
        ret = []
        while not done:
            r = parse(self.arg)
            if not is_bad_parse(r):
                ret.append(r)
            else:
                done = True
        self.result = ret
        return ret

class OneOrMore_ob(object):
    def __init__(self, arg):
        self.arg = arg

    def parse(self):
        return parse(Each(self.arg, ZeroOrMore(self.arg)))

def literal(*args):
    return lambda: literal_ob(*args)
class literal_ob(object):
    def __init__(self, regex):
        self.regex = regex

    def parse(self):
        self.result = try_consume(self.regex)
        return self.result

def indent_all(text, num=1):
    return "\n".join([("    "*num) + s for s in text.splitlines()])

word = "[a-zA-Z0-9_]+"
equals = "="
comma = ","
open_paren = "\("
close_paren = "\)"
open_brace = "{"
close_brace = "}"
semicolon = ";"
backtick = "`[^`]+`"
return_word = "return"
string = "\"[^\"]*\""
open_bracket = "\["
close_bracket = "\]"
period = "\."

literals = [word, equals, comma, open_paren, close_paren, open_brace, close_brace, semicolon, backtick, return_word, string, open_bracket, close_bracket, period]

def parse(ob):
    if isinstance(ob, str):
        ob = literal(ob)
    ob = ob()
    if hasattr(ob, 'defn'): # TODO: reflection is bad..
        defn = ob.defn()
        ob.result = parse(defn)
    else:
        ob.result = ob.parse()
    if is_bad_parse(ob.result):
        return None
    return ob

class assignable_value(object):
    def defn(self):
        return Or(string_def, array_def, array_ref, statement, word)

class assignment(object):
    def defn(self):
        return Each(word, equals, assignable_value)

    def tocode(self):
        # TODO: result.result is weird
        return tocode(self.result.result[0]) + " = " + tocode(self.result.result[2])

class remaining_arg(object):
    def defn(self):
        return Each(comma, word)

class arg_list(object):
    def defn(self):
        return ZeroOrOne(Each(word, ZeroOrMore(remaining_arg)))

class function_definition(object):
    def defn(self):
        return Each(word, equals, open_paren, arg_list, close_paren, open_brace, statements, close_brace)

    def tocode(self):
        class_name = tocode(self.result.result[0])
        arg_list = tocode(self.result.result[3])
        method_body = tocode(self.result.result[6])

        ret = "class " + class_name + "():\n"
        ret += "    def invoke(self, " + arg_list + "):\n"
        ret += "        self.final_result = self\n" # if there's no return statement, it's a constructor
        inner = tocode(self.result.result[6])
        if inner:
            ret = ret + indent_all(method_body, 2)
        else:
            ret = ret + indent_all("pass", 2)
        ret += "\n" # TODO: why is this needed?
        ret += indent_all("return self", 2)
        ret += "\n" + class_name + " = " + class_name + "()"
        ret += "\nself." + class_name + " = " + class_name
        return ret

class function_invocation(object):
    def defn(self):
        return Each(word, open_paren, arg_list, close_paren)

    def tocode(self):
        function_name = tocode(self.result.result[0])
        args = tocode(self.result.result[2])

        return function_name + ".invoke(" + args + ").final_result"

class method_invocation(object):
    def defn(self):
        return Each(word, period, function_invocation)

class invoke_system(object):
    def defn(self):
        return Each(backtick, ZeroOrOne(Each(open_paren, arg_list, close_paren)))

    def tocode(self):
        # TODO: wow. Should be self.result[1]
        assembly_var = repr(self.result.result[1].result.result[1].result.result.result[0].result)
        command = tocode(self.result.result[0])
        command = command[1:-1] # strip backticks
        command = command.replace("{", "\" + ")
        command = command.replace("}", " + \"")
        return "p = subprocess.Popen(\"" + command + "\", stdin=subprocess.PIPE, shell=True)\np.communicate(input=" + assembly_var + ")"

class string_def(object):
    def defn(self):
        return string

class array_def(object):
    def defn(self):
        return Each(open_bracket, arg_list, close_bracket)

class array_ref(object):
    def defn(self):
        return Each(word, open_bracket, assignable_value, close_bracket)
    def tocode(self):
        ret = ""
        ary = tocode(self.result.result[0])
        if ary == "args":
            ary = "sys.argv"
        ret += ary
        ret += tocode(self.result.result[1:4])
        return ret

class return_stmt(object):
    def defn(self):
        return Each(return_word, assignable_value)

    def tocode(self):
        returning = tocode(self.result.result[1])
        ret = "self.final_result = " + returning
        return ret

class statement(object):
    def defn(self):
        return Or(function_definition, function_invocation, method_invocation, assignment, invoke_system, return_stmt)

class statement_with_semi(object):
    def defn(self):
        return Each(statement, semicolon)

    def tocode(self):
        return tocode(self.result.result[0]) + "\n" # strip semis

class statements(object):
    def defn(self):
        return ZeroOrMore(statement_with_semi)

class program(object):
    def defn(self):
        return statements

    def tocode(self):
        ret = """#!/usr/bin/env python
import sys
import os
import subprocess

class read_file(object):
    def invoke(self, arg):
        with open(arg) as f:
            self.final_result = f.read()
            return self
read_file = read_file()

class everything(object):
    def invoke(self):
"""
        ret += indent_all(tocode(self.result), 2)
        ret += "\neverything().invoke()"
        return ret


def remove_comments(string):
    return re.sub('#.*', '', string)

def tocode(element):
    if element is None:
        return ""
    if isinstance(element, list):
        ret = ""
        for item in element:
            ret += tocode(item)
        return ret
    if hasattr(element, 'tocode'): # TODO: reflection is bad
        return element.tocode()
    return tocode(element.result)

contents = remove_comments(contents)

all_literals = "|".join(literals)
tokens = re.findall(all_literals, contents)
position = 0
parsed = parse(program)
if position < len(tokens):
    print "Parse error: tokens left, position is ", position
    print tokens[position:]

with open(outfile, "w") as f:
    f.write(parsed.tocode())

os.chmod(outfile, 0755)
