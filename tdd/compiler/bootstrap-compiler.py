#!/usr/bin/env python

import sys
import os
import re

outfile = sys.argv[2]
infile = sys.argv[3]

with open(infile) as f:
    contents = f.read()

# assignment = variable "=" value ";"

# TODO: globals are bad...

token = None
def try_consume(regex):
    global position
    global token
    token = tokens[position]
    if re.match(regex, token):
        position += 1
        return True
    return False

def backtrack(fn):
    def wrapper(*args, **kwargs):
        global position
        orig_position = position
        result = fn(*args, **kwargs)
        if not result:
            position = orig_position
        return result
    return wrapper

def Or(*args):
    for item in args:
        if item():
            return True
    return False

def Each(*args):
    for item in args:
        if not item():
            return False
    return True

word = lambda: try_consume("[a-z\[\]]+") # TODO: lambda and try_consume are dup'd
equals = lambda: try_consume("=")

assignment = lambda: Each(word, equals, lambda: Or(statement, word))

@backtrack
def arg_list():
    if not try_consume("[a-z]+"):
        return False

    arg = token

    while remaining_arg():
        pass
    return True

@backtrack
def remaining_arg():
    if not try_consume(","):
        return False

    if not try_consume("[a-z]+"):
        return False

    arg = token

    return True

@backtrack
def function_definition():
    if not try_consume("[a-z]+"):
        return False

    fn_name = token

    if not try_consume("="):
        return False

    if not try_consume("\("):
        return False

    if not arg_list():
        return False

    if not try_consume("\)"):
        return False

    if not try_consume("{"):
        return False

    if not statements():
        return False

    if not try_consume("}"):
        return False

    return True

@backtrack
def function_invocation():
    if not try_consume("[a-z]+"):
        return False

    global token
    fn_name = token

    if not try_consume("\("):
        return False

    if not arg_list():
        return False

    if not try_consume("\)"):
        return False

    print fn_name + "()"
    return True

@backtrack
def statement():
    if function_definition():
        return True
    if function_invocation():
        return True
    if assignment():
        return True

    return False

@backtrack
def statements():
    done = False
    while not done:
        if position < len(tokens):
            done = True
            if statement():
                if try_consume(";"):
                    done = False
        else:
            done = True
    return True

def remove_comments(string):
    return re.sub('#.*', '', string)

contents = remove_comments(contents)

tokens = re.findall("[a-z0-9\[\]_]+|=|;|\(|\)|,|{|}|`", contents)
position = 0
statements()
if position < len(tokens):
    print "Parse error: tokens left, position is ", position

with open(outfile, "w") as f:
    f.write("")

os.chmod(outfile, 0755)
