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

class Or(object):
    def __init__(self, *args):
        self.args = args

    @backtrack
    def parse(self):
        for item in self.args:
            r = item().parse()
            if not is_bad_parse(r):
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
            r = item().parse()
            if is_bad_parse(r):
                return r
            ret.append(r)

        self.result = ret
        return ret

class ZeroOrOne(object):
    def __init__(self, arg):
        self.arg = arg

    def parse(self):
        r = self.arg().parse()
        if is_bad_parse(r):
            self.result = []
            return []
        self.result = r
        return r

class ZeroOrMore(object):

    def __init__(self, arg):
        self.arg = arg

    def parse(self):
        done = False
        ret = []
        while not done:
            r = self.arg().parse()
            if not is_bad_parse(r):
                ret.append(r)
            else:
                done = True
        self.result = ret
        return ret

class OneOrMore(object):
    def __init__(self, arg):
        self.arg = arg

    def parse(self):
        return Each(self.arg, lambda: ZeroOrMore(self.arg)).parse()

class literal(object):
    def __init__(self, regex):
        self.regex = regex

    def parse(self):
        return try_consume(self.regex)

# TODO: "lambda" dup'd
word = lambda: literal("[a-z\[\]]+") # TODO: "literal" dup'd
equals = lambda: literal("=")
comma = lambda: literal(",")
open_paren = lambda: literal("\(")
close_paren = lambda: literal("\)")
open_brace = lambda: literal("{")
close_brace = lambda: literal("}")
semicolon = lambda: literal(";")
backtick = lambda: literal("`[^`]+`");

def parse(ob):
    ob.result = ob.defn().parse()
    if is_bad_parse(ob.result):
        return None
    return ob

# TODO: class boilerplate dup'd
# TODO: literals don't have () but classes do (neither should, really)
class assignment(object):
    def defn(self):
        return Each(word, equals, lambda: Or(statement, word)) # TODO: 'lambda' shouldn't be there

    def parse(self): # TODO: boilerplate
        r = parse(self)
        return r

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
        return ZeroOrOne(lambda: Each(word, lambda: ZeroOrMore(remaining_arg)))

    def parse(self):
        return parse(self)

    def tocode(self):
        return tocode(self.result)

class function_definition(object):
    def defn(self):
        return Each(word, equals, open_paren, arg_list, close_paren, open_brace, statements, close_brace)

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
        return Each(word, open_paren, arg_list, close_paren)

    def parse(self):
        return parse(self)

    def tocode(self):
        return indent + tocode(self.result) # TODO: statement should be the only thing with indent on it...

class invoke_system(object):
    def defn(self):
        return backtick()

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
        return Or(function_definition, function_invocation, assignment, invoke_system)

    def parse(self):
        return parse(self)

    def tocode(self):
        r = tocode(self.result)
        return r

class statement_with_semi(object):
    def defn(self):
        return Each(statement, semicolon)

    def parse(self):
        r = parse(self)
        return r

    def tocode(self):
        r = tocode(self.result[0]) + "\n" # strip semis
        return r

class statements(object):
    def defn(self):
        return ZeroOrMore(statement_with_semi)

    def parse(self):
        r = parse(self)
        return r

    def tocode(self):
        r = tocode(self.result)
        return r

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
parsed = parse(program())
if position < len(tokens):
    print "Parse error: tokens left, position is ", position
    print tokens[position:]

with open(outfile, "w") as f:
    f.write(parsed.tocode())

os.chmod(outfile, 0755)
