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
    def __init__(self, result):
        self.result = result
    def parse(self):
        return self.result
    def tocode(self):
        if self.result == "args[2]":
            return "sys.argv[2]"
        if self.result == "args[3]":
            return "sys.argv[3]"
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

def backtrack(fn):
    def wrapper(*args, **kwargs):
        global position
        orig_position = position
        result = fn(*args, **kwargs)
        if result is None:
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
            if r is not None and r.result is not None:
                self.result = r
                return r
        return None

class Each(object):
    def __init__(self, *args):
        self.args = args

    @backtrack
    def parse(self):
        ret = []
        for item in self.args:
            r = item.parse()
            if r is None:
                return r
            ret.append(r)

        return ret

class ZeroOrOne(object):
    def __init__(self, arg):
        self.arg = arg

    def parse(self):
        r = self.arg.parse()
        if r is None:
            return []
        return r

class ZeroOrMore(object):

    def __init__(self, arg):
        self.arg = arg

    def parse(self):
        done = False
        ret = []
        while not done:
            r = self.arg.parse()
            if r is not None:
                ret.append(r)
            else:
                done = True
        return ret

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

word = literal("[a-z\[\]]+") # TODO: "literal" dup'd
equals = literal("=")
comma = literal(",")
open_paren = literal("\(")
close_paren = literal("\)")
open_brace = literal("{")
close_brace = literal("}")
semicolon = literal(";")
backtick = literal("`[^`]+`");

def parse(ob):
    ob.result = ob.defn().parse()
    if ob.result is None:
        return None
    return ob

# TODO: class boilerplate dup'd
# TODO: literals don't have () but classes do (neither should, really)
class assignment(object):
    def defn(self):
        return Each(word, equals, Or(statement(), word))

    def parse(self): # TODO: boilerplate
        return parse(self)

    def tocode(self):
        return indent + tocode(self.result[0]) + " = " + tocode(self.result[2])

class remaining_arg(object):
    def defn(self):
        return Each(comma, word)

    def parse(self):
        return parse(self)

    def tocode(self): # TODO: lots of these dup'd
        return tocode(self.result)

class arg_list(object):
    def defn(self):
        return ZeroOrOne(Each(word, ZeroOrMore(remaining_arg())))

    def parse(self):
        return parse(self)

    def tocode(self):
        return tocode(self.result)

class function_definition(object):
    def defn(self):
        return Each(word, equals, open_paren, arg_list(), close_paren, open_brace, statements(), close_brace)

    def parse(self):
        return parse(self)

    def tocode(self):
        global indent
        indent += "    "
        ret = "def " + tocode(self.result[0]) + "(" + tocode(self.result[3]) + "):\n" + tocode(self.result[6]) + indent + "pass"
        indent = indent[4:]
        return ret

class function_invocation(object):
    def defn(self):
        return Each(word, open_paren, arg_list(), close_paren)

    def parse(self):
        return parse(self)

    def tocode(self):
        return indent + tocode(self.result) # TODO: statement should be the only thing with indent on it...

class invoke_system(object):
    def defn(self):
        return backtick

    def parse(self):
        return parse(self)

    def tocode(self):
        global indent
        command = tocode(self.result)
        command = command[1:-1] # strip backticks
        command = command.replace("{", "\" + ")
        command = command.replace("}", " + \"")
        return indent + "os.system(\"" + command + "\")"

class statement(object):
    def defn(self):
        return Or(function_definition(), function_invocation(), assignment(), invoke_system())

    def parse(self):
        return parse(self)

    def tocode(self):
        return tocode(self.result)

class statement_with_semi(object):
    def defn(self):
        return Each(statement(), semicolon)

    def parse(self):
        self.result = self.defn().parse()
        return self.result # TODO: should be 'return self' (actually should be like the other parse methods) (actually the whole method should be gone)

    def tocode(self):
        return tocode(self.result)

class statements(object):
    def defn(self):
        return ZeroOrMore(statement_with_semi())

    def parse(self):
        return parse(self)

    def tocode(self):
        ret = ""
        for stmt_with_semi in self.result:
            ret += tocode(stmt_with_semi[0]) + "\n" # strip semicolons
        return ret

class program(object):
    def defn(self):
        return statements()

    def parse(self):
        return parse(self)

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
