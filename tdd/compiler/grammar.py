
import unittest2
import re

def indent(string):
    ret = ""
    lines = string.splitlines()
    for line in lines:
        ret += "    " + line + "\n"
    return ret

class ParseResult(object):
    def __init__(self, literal_value):
        self.literal_value = literal_value
        self.matchlen = len(self.literal_value)

    def tocode(self):
        return self.literal_value

class EOF(object):
    def __init__(self):
        self.matchlen = 0

    def parse(self, code):
        if code == '':
            return self
        return None

class RegexParser(object):
    def __init__(self, regex):
        self.regex = regex

    def parse(self, code):
        match = re.match(self.regex, code)
        if match:
            #print code
            #print "matched", self.regex
            literal_value = match.group(0)
            return ParseResult(literal_value)

class Or(object):
    def __init__(self, *args):
        self.items = args

    def parse(self, code):
        for parser in self.items:
            parse_result = parser.parse(code)
            if parse_result is not None:
                return parse_result

class ResultList(object):
    def __init__(self, items):
        self.items = items
        total_matchlen = 0
        for item in items:
            total_matchlen += item.matchlen
        self.matchlen = total_matchlen

    def tocode(self):
        code = ""
        for item in self.items:
            code += item.tocode()
        return code

    def __getitem__(self, key):
        return self.items[key]

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return "ResultList(" + repr(self.items) + ")"

class ZeroOrMore(object):
    def __init__(self, arg):
        self.item = arg

    def parse(self, code):
        results = []
        while(True):
            result = self.item.parse(code)
            if result is None:
                return ResultList(results)
            code = code[result.matchlen:]
            results.append(result)

class OneOrMore(object):
    def __init__(self, arg):
        self.item = arg

    def parse(self, code):
        return Each(self.item, ZeroOrMore(self.item)).parse(code)

class ZeroOrOne(object):
    def __init__(self, arg):
        self.item = arg

    def parse(self, code):
        result = self.item.parse(code)
        if result is None:
            return ResultList([])
        return ResultList([result])

class Each(object):
    def __init__(self, *args):
        self.items = args

    def parse(self, code):
        results = []
        for item in self.items:
            parse_result = item.parse(code)
            if parse_result is None:
                return None
            results.append(parse_result)
            code = code[parse_result.matchlen:]

        return ResultList(results)

class GrammarElementResult(object):
    def __init__(self, inner, result):
        self.result = result
        self.inner = inner
        self.matchlen = result.matchlen

    def tocode(self):
        return self.inner.tocode(self.result)

class GrammarElement(object):
    def __init__(self, inner):
        self.inner = inner()

    def defn(self):
        return self.inner.defn()

    def make_result(self, result):
        return GrammarElementResult(self.inner, result)

    def parse(self, code):
        result = self.defn().parse(code)
        if result is None:
            return None
        return self.make_result(result)
