#!/usr/bin/env python

import sys
import os
import re

outfile = sys.argv[2]
infile = sys.argv[3]

with open(infile) as f:
    contents = f.read()

# TODO: globals are bad, make a class so they can be instance variables instead

class SingleToken(object):
    def __init__(self, result):
        self.result = result
    def tocode(self):
        if self.result == "args[2]":
            return "sys.argv[2]"
        if self.result == "args[3]":
            return "sys.argv[3]"
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

def indent_all(text):
    return "\n".join(["    " + s for s in text.splitlines()])

word = "[a-z0-9\[\]_]+"
equals = "="
comma = ","
open_paren = "\("
close_paren = "\)"
open_brace = "{"
close_brace = "}"
semicolon = ";"
backtick = "`[^`]+`"
return_word = "return"

literals = [word, equals, comma, open_paren, close_paren, open_brace, close_brace, semicolon, backtick, return_word]

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

class assignment(object):
    def defn(self):
        return Each(word, equals, Or(statement, word))

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
        ret = "def " + tocode(self.result.result[0]) + "(" + tocode(self.result.result[3]) + "):\n"
        ret = ret + indent_all(tocode(self.result.result[6]) + "pass")
        return ret

class function_invocation(object):
    def defn(self):
        return Each(word, open_paren, arg_list, close_paren)

class invoke_system(object):
    def defn(self):
        return backtick

    def tocode(self):
        command = tocode(self.result)
        command = command[1:-1] # strip backticks
        command = command.replace("{", "\" + ")
        command = command.replace("}", " + \"")
        return "os.system(\"" + command + "\")"

class return_stmt(object):
    def defn(self):
        return Each(return_word, statement)

    def tocode(self):
        return tocode(self.result.result[0]) + " " + tocode(self.result.result[1])

class statement(object):
    def defn(self):
        return Or(function_definition, function_invocation, assignment, invoke_system, return_stmt)

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
        ret = "#!/usr/bin/env python\nimport sys\nimport os\n"
        ret += tocode(self.result)
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
