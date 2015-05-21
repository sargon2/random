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

def try_consume(position, regex):
    if not re.match(regex, tokens[position]):
        # TODO: don't raise, use return code? Or is raising the right answer?
        raise ParseWrong("Expected " + regex + ", got " + tokens[position])

def assignment(position):
    try_consume(position, "[a-z]+")
    variable = tokens[position]
    position += 1

    try_consume(position, "=")
    position += 1

    position = statement(position)

    return position

def arg_list(position):
    try_consume(position, "[a-z]+")
    arg = tokens[position]
    position += 1

    done = False
    while not done:
        try:
            position = remaining_arg(position)
        except ParseWrong:
            done = True
        except:
            raise
    return position

def remaining_arg(position):
    try_consume(position, ",")
    position += 1

    try_consume(position, "[a-z]+")
    arg = tokens[position]
    position += 1

    return position

def function_definition(position):
    try_consume(position, "[a-z]+")
    fn_name = tokens[position]
    position += 1

    try_consume(position, "=")
    position += 1

    try_consume(position, "\(")
    position += 1

    position = arg_list(position)

    try_consume(position, "\)")
    position += 1

    try_consume(position, "{")
    position += 1

    position = statements(position)

    try_consume(position, "}")
    position += 1

    return position

def function_invocation(position):
    try_consume(position, "[a-z]+")
    fn_name = tokens[position]
    position += 1

    try_consume(position, "\(")
    position += 1

    position = arg_list(position)

    try_consume(position, "\)")
    position += 1

    return position

def statement(position):
    # TODO: this shouldn't be nested
    try:
        position = function_definition(position)
    except ParseWrong:
        try:
            position = function_invocation(position)
        except ParseWrong:
            try:
                position = assignment(position)
            except ParseWrong:
                try:
                    try_consume(position, "[a-z\[\]]+")
                    position += 1
                except ParseWrong:
                    raise

    return position


def statements(position):
    done = False
    while not done:
        if position < len(tokens):
            try:
                position = statement(position)
                try_consume(position, ";")
                position += 1

            except ParseWrong:
                done = True
            except:
                raise
        else:
            done = True
    return position

def remove_comments(string):
    return re.sub('#.*', '', string)

contents = remove_comments(contents)

tokens = re.findall("[a-z0-9\[\]_]+|=|;|\(|\)|,|{|}|`", contents)
try:
    position = statements(0)
except ParseWrong as e:
    print "Parse error:", e
else:
    if position < len(tokens):
        print "Parse error: tokens left, position is ", position

with open(outfile, "w") as f:
    f.write("")

os.chmod(outfile, 0755)
