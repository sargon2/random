#!/usr/bin/env python

import sys
import os
import re

outfile = sys.argv[2]
infile = sys.argv[3]

with open(infile) as f:
    contents = f.read()

# assignment = variable "=" value ";"

class ParseWrong(BaseException):
    pass

# TODO: instead of passing around the modified token list, pass around an index into the (immutable) token list

def try_consume(token, regex):
    if re.match(regex, token):
        return token
    # TODO: don't raise, use return code? or return an object that contains token and bool 'matched'?
    # Or is raising the right answer?
    raise ParseWrong("Expected " + regex + ", got " + token)

def assignment(tokens):
    variable = try_consume(tokens[0], "[a-z]+")
    tokens = tokens[1:]

    try_consume(tokens[0], "=")
    tokens = tokens[1:]

    tokens = statement(tokens)

    return tokens

def arg_list(tokens):
    arg = try_consume(tokens[0], "[a-z]+")
    tokens = tokens[1:]

    done = False
    while not done:
        try:
            tokens = remaining_arg(tokens)
        except ParseWrong:
            done = True
        except:
            raise
    return tokens

def remaining_arg(tokens):
    try_consume(tokens[0], ",")
    tokens = tokens[1:]

    arg = try_consume(tokens[0], "[a-z]+")
    tokens = tokens[1:]

    return tokens

def function_definition(tokens):
    fn_name = try_consume(tokens[0], "[a-z]+")
    tokens = tokens[1:]

    try_consume(tokens[0], "=")
    tokens = tokens[1:]

    try_consume(tokens[0], "\(")
    tokens = tokens[1:]

    tokens = arg_list(tokens)

    try_consume(tokens[0], "\)")
    tokens = tokens[1:]

    try_consume(tokens[0], "{")
    tokens = tokens[1:]

    tokens = statements(tokens)

    try_consume(tokens[0], "}")
    tokens = tokens[1:]

    return tokens

def function_invocation(tokens):
    fn_name = try_consume(tokens[0], "[a-z]+")
    tokens = tokens[1:]

    try_consume(tokens[0], "\(")
    tokens = tokens[1:]

    tokens = arg_list(tokens)

    try_consume(tokens[0], "\)")
    tokens = tokens[1:]

    return tokens

def statement(tokens):
    # TODO: this shouldn't be nested
    try:
        tokens = function_definition(tokens)
    except ParseWrong:
        try:
            tokens = function_invocation(tokens)
        except ParseWrong:
            try:
                tokens = assignment(tokens)
            except ParseWrong:
                try:
                    try_consume(tokens[0], "[a-z\[\]]+")
                    tokens = tokens[1:]
                except ParseWrong:
                    raise

    return tokens


def statements(tokens):
    done = False
    while not done:
        if tokens:
            try:
                tokens = statement(tokens)
                try_consume(tokens[0], ";")
                tokens = tokens[1:]

            except ParseWrong:
                done = True
            except:
                raise
        else:
            done = True
    return tokens

def remove_comments(string):
    return re.sub('#.*', '', string)

contents = remove_comments(contents)

tokens = re.findall("[a-z0-9\[\]_]+|=|;|\(|\)|,|{|}|`", contents)
try:
    tokens = statements(tokens)
except ParseWrong as e:
    print "Parse error:", e
else:
    if tokens:
        print "Parse error: tokens left", tokens

with open(outfile, "w") as f:
    f.write("")

os.chmod(outfile, 0755)
