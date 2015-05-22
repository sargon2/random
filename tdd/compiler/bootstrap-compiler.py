#!/usr/bin/env python

import sys
import os
import re

outfile = sys.argv[2]
infile = sys.argv[3]

with open(infile) as f:
    contents = f.read()

# TODO: globals are bad...

class SingleToken(object):
    def __init__(self, token):
        self.token = token
    def get(self):
        return self.token
    def __repr__(self):
        return "\"" + self.token + "\""

class Falsy(object):
    def get(self):
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
        if result == False or isinstance(result, Falsy):
            position = orig_position
        return result
    return wrapper

class Or(object):
    def __init__(self, *args):
        self.args = args

    @backtrack
    def get(self):
        for item in self.args:
            r = item.get()
            if not r == False and not isinstance(r, Falsy):
                return r
        return Falsy()

class Each(object):
    def __init__(self, *args):
        self.args = args

    @backtrack
    def get(self):
        ret = []
        for item in self.args:
            r = item.get()
            if r == False or isinstance(r, Falsy):
                return Falsy()
            ret.append(r)
        return ret

class ZeroOrMore(object):

    def __init__(self, arg):
        self.arg = arg

    def get(self):
        done = False
        ret = []
        while not done:
            r = self.arg.get()
            if not r == False and not isinstance(r, Falsy):
                ret.append(r)
            else:
                done = True
        return ret

class Literal(object):
    def __init__(self, regex):
        self.regex = regex

    def get(self):
        return try_consume(self.regex)

word = Literal("[a-z\[\]]+") # TODO: "Literal" dup'd
equals = Literal("=")
comma = Literal(",")
open_paren = Literal("\(")
close_paren = Literal("\)")
open_brace = Literal("{")
close_brace = Literal("}")
semicolon = Literal(";")

# TODO: class boilerplate dup'd
# TODO: literals don't have () but classes do (neither should, really)
# TODO: "get" is a terrible function name
class assignment(object):
    def get(self):
        return Each(word, equals, Or(statement(), word)).get()

class remaining_arg(object):
    def get(self):
        return Each(comma, word).get()

class arg_list(object):
    def get(self):
        return Each(word, ZeroOrMore(remaining_arg())).get()

class function_definition(object):
    def get(self):
        return Each(word, equals, open_paren, arg_list(), close_paren, open_brace, statements(), close_brace).get()

class function_invocation(object):
    def get(self):
        return Each(word, open_paren, arg_list(), close_paren).get()

class statement(object):
    def get(self):
        return Or(function_definition(), function_invocation(), assignment()).get()

class statement_with_semi(object):
    def get(self):
        return Each(statement(), semicolon).get()

class statements(object):
    def get(self):
        return ZeroOrMore(statement_with_semi()).get()


def remove_comments(string):
    return re.sub('#.*', '', string)

contents = remove_comments(contents)

tokens = re.findall("[a-z0-9\[\]_]+|=|;|\(|\)|,|{|}|`", contents) # TODO: dup'd with literals above
position = 0
parsed = statements().get()
if position < len(tokens):
    print "Parse error: tokens left, position is ", position
print parsed

with open(outfile, "w") as f:
    f.write("")

os.chmod(outfile, 0755)
