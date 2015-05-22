#!/usr/bin/env python

import sys
import os
import re

outfile = sys.argv[2]
infile = sys.argv[3]

with open(infile) as f:
    contents = f.read()

# TODO: globals are bad...

token = None
def try_consume(regex):
    global position
    global token
    if position >= len(tokens):
        return False
    token = tokens[position]
    if re.match(regex, token):
        position += 1
        return [token]
    return False

def backtrack(fn):
    def wrapper(*args, **kwargs):
        global position
        orig_position = position
        result = fn(*args, **kwargs)
        if  result == False:
            position = orig_position
        return result
    return wrapper

@backtrack
def Or(*args):
    for item in args:
        r = item()
        if r != False:
            return r
    return False

@backtrack
def Each(*args):
    ret = []
    for item in args:
        r = item()
        if r == False:
            return False
        ret.extend(r)
    return ret

def ZeroOrMore(arg):
    done = False
    ret = []
    while not done:
        r = arg()
        if r != False:
            ret.append(r)
        else:
            done = True
    return ret

def Literal(regex):
    return lambda: try_consume(regex)

word = Literal("[a-z\[\]]+") # TODO: "Literal" dup'd
equals = Literal("=")
comma = Literal(",")
open_paren = Literal("\(")
close_paren = Literal("\)")
open_brace = Literal("{")
close_brace = Literal("}")
semicolon = Literal(";")

# TODO: too many lambda keywords...
assignment = lambda: Each(word, equals, lambda: Or(statement, word))
remaining_arg = lambda: Each(comma, word)
arg_list = lambda: Each(word, lambda: ZeroOrMore(remaining_arg))
function_definition = lambda: Each(word, equals, open_paren, arg_list, close_paren, open_brace, statements, close_brace)
function_invocation = lambda: Each(word, open_paren, arg_list, close_paren)
statement = lambda: Or(function_definition, function_invocation, assignment)
statement_with_semi = lambda: Each(statement, semicolon)
statements = lambda: ZeroOrMore(statement_with_semi)


def remove_comments(string):
    return re.sub('#.*', '', string)

contents = remove_comments(contents)

tokens = re.findall("[a-z0-9\[\]_]+|=|;|\(|\)|,|{|}|`", contents) # TODO: dup'd with literals above
position = 0
parsed = statements()
if position < len(tokens):
    print "Parse error: tokens left, position is ", position
print parsed

with open(outfile, "w") as f:
    f.write("")

os.chmod(outfile, 0755)
