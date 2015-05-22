#!/usr/bin/env python

import sys
import os
import re

outfile = sys.argv[2]
infile = sys.argv[3]

with open(infile) as f:
    contents = f.read()

# TODO: globals are bad...

indent = ""

class SingleToken(object):
    def __init__(self, token):
        self.token = token
    def parse(self):
        return self.token
    def __repr__(self):
        return "\"" + self.token + "\""
    def tocode(self):
        if self.token == "args[2]":
            return "sys.argv[2]"
        if self.token == "args[3]":
            return "sys.argv[3]"
        return self.token

class Falsy(object):
    def parse(self):
        return Falsy()

token = None
def try_consume(regex):
    global position
    global token
    if position >= len(tokens):
        return Falsy()
    token = tokens[position]
    if re.match(regex, token):
        position += 1
        return SingleToken(token)
    return Falsy()

def backtrack(fn):
    def wrapper(*args, **kwargs):
        global position
        orig_position = position
        result = fn(*args, **kwargs)
        if isinstance(result, Falsy):
            position = orig_position
        return result
    return wrapper

class Or(object):
    def __init__(self, *args):
        self.args = args

    @backtrack
    def parse(self):
        for item in self.args:
            r = item.parse()
            if not isinstance(r, Falsy):
                self.result = r
                return r
        return Falsy()

class Each(object):
    def __init__(self, *args):
        self.args = args

    @backtrack
    def parse(self):
        ret = []
        for item in self.args:
            r = item.parse()
            if isinstance(r, Falsy):
                return Falsy()
            ret.append(r)

        return ret

    def __repr__(self):
        return "Each: " + str(self.result)

class ZeroOrMore(object):

    def __init__(self, arg):
        self.arg = arg

    def parse(self):
        done = False
        ret = []
        while not done:
            r = self.arg.parse()
            if not isinstance(r, Falsy):
                ret.append(r)
            else:
                done = True
        return ret

    def __repr__(self):
        return "Or: " + str(self.item)

class OneOrMore(object):
    def __init__(self, arg):
        self.arg = arg

    def parse(self):
        return Each(self.arg, ZeroOrMore(self.arg)).parse()

class literal(object):
    def __init__(self, regex):
        self.regex = regex

    def parse(self):
        return try_consume(self.regex)

    def __repr__(self):
        return str(self.item)

word = literal("[a-z\[\]]+") # TODO: "literal" dup'd
equals = literal("=")
comma = literal(",")
open_paren = literal("\(")
close_paren = literal("\)")
open_brace = literal("{")
close_brace = literal("}")
semicolon = literal(";")
backtick = literal("`[^`]+`");

# TODO: class boilerplate dup'd
# TODO: literals don't have () but classes do (neither should, really)
# TODO: return objects instead of lists
class assignment(object):
    def parse(self):
        self.result = Each(word, equals, Or(statement(), word)).parse()
        if isinstance(self.result, Falsy):
            return self.result
        return self

    def __repr__(self):
        return "Assignment: " + str(self.result)

    def tocode(self):
        return indent + tocode(self.result[0]) + " = " + tocode(self.result[2])

class remaining_arg(object):
    def parse(self):
        return Each(comma, word).parse()

class arg_list(object):
    def parse(self):
        return Each(word, ZeroOrMore(remaining_arg())).parse()

class function_definition(object):
    def parse(self):
        self.result = Each(word, equals, open_paren, arg_list(), close_paren, open_brace, statements(), close_brace).parse()
        if isinstance(self.result, Falsy): # TODO: lots of these checks dup'd
            return self.result
        return self

    def tocode(self):
        global indent
        indent += "    "
        ret = "def " + tocode(self.result[0]) + "(" + tocode(self.result[3]) + "):\n" + tocode(self.result[6]) + indent + "pass"
        indent = indent[4:]
        return ret

class function_invocation(object):
    def parse(self):
        return Each(word, open_paren, arg_list(), close_paren).parse()

class invoke_system(object):
    def parse(self):
        self.result = backtick.parse()
        if isinstance(self.result, Falsy):
            return self.result
        return self
    def tocode(self):
        global indent
        command = tocode(self.result)
        command = command[1:-1] # strip backticks
        command = command.replace("{", "\" + ")
        command = command.replace("}", " + \"")
        return indent + "os.system(\"" + command + "\")"

class statement(object):
    def parse(self):
        return Or(function_definition(), function_invocation(), assignment(), invoke_system()).parse()

class statement_with_semi(object):
    def parse(self):
        return Each(statement(), semicolon).parse()

class statements(object):
    def parse(self):
        self.result = ZeroOrMore(statement_with_semi()).parse()
        if isinstance(self.result, Falsy):
            return self.result
        return self
    def __repr__(self):
        return "statements: " + str(self.result)
    def tocode(self):
        ret = ""
        for stmt_with_semi in self.result:
            ret += tocode(stmt_with_semi[0]) + "\n" # strip semicolons
        return ret

class program(object):
    def parse(self):
        self.result = statements().parse()
        if isinstance(self.result, Falsy):
            return self.result
        return self

    def tocode(self):
        ret = "#!/usr/bin/env python\nimport sys\nimport os\n"
        ret += tocode(self.result)
        return ret


def remove_comments(string):
    return re.sub('#.*', '', string)

def tocode(element):
    if isinstance(element, list):
        ret = ""
        for item in element:
            ret += tocode(item)
        return ret
    return element.tocode()

contents = remove_comments(contents)

tokens = re.findall("[a-z0-9\[\]_]+|=|;|\(|\)|,|{|}|`[^`]+`", contents) # TODO: dup'd with literals above
position = 0
s = program()
s.parse()
parsed = s
if position < len(tokens):
    print "Parse error: tokens left, position is ", position
    print tokens[position:]

with open(outfile, "w") as f:
    f.write(parsed.tocode())

os.chmod(outfile, 0755)
