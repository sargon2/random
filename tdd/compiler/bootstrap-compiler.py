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

def Or(*args):
    for item in args:
        r = item()
        if r != False:
            return r
    return False

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

word = lambda: try_consume("[a-z\[\]]+") # TODO: lambda and try_consume are dup'd
equals = lambda: try_consume("=")
comma = lambda: try_consume(",")
open_paren = lambda: try_consume("\(")
close_paren = lambda: try_consume("\)")
open_brace = lambda: try_consume("{")
close_brace = lambda: try_consume("}")
semicolon = lambda: try_consume(";")

assignment = lambda: Each(word, equals, lambda: Or(statement, word))

remaining_arg = lambda: Each(comma, word)

arg_list = lambda: Each(word, lambda: ZeroOrMore(remaining_arg))

@backtrack # TODO: get rid of decorator
def function_definition():
    return Each(word, equals, open_paren, arg_list, close_paren, open_brace, statements, close_brace)

@backtrack
def function_invocation():
    return Each(word, open_paren, arg_list, close_paren)

@backtrack
def statement():
    return Or(function_definition, function_invocation, assignment)

statement_with_semi = lambda: Each(statement, semicolon)

statements = lambda: ZeroOrMore(statement_with_semi)


def remove_comments(string):
    return re.sub('#.*', '', string)

contents = remove_comments(contents)

tokens = re.findall("[a-z0-9\[\]_]+|=|;|\(|\)|,|{|}|`", contents)
position = 0
parsed = statements()
if position < len(tokens):
    print "Parse error: tokens left, position is ", position
print parsed

with open(outfile, "w") as f:
    f.write("")

os.chmod(outfile, 0755)
