import re

def indent(string):
    ret = ""
    lines = string.splitlines()
    for line in lines:
        ret += "    " + line + "\n"
    return ret

class ParseResult(object):
    def __init__(self, literal_value, match_ob=None):
        self.literal_value = literal_value
        self.matchlen = len(self.literal_value)
        self.match_ob = match_ob

    def tocode(self):
        return self.literal_value

    def __repr__(self):
        return "ParseResult(\"" + self.literal_value + "\")"

class EOF(object):
    def __init__(self):
        self.matchlen = 0

    def parse(self, code):
        if code == '':
            return self
        return None

class Regex(object):
    def __init__(self, regex):
        self.regex = regex

    def parse(self, code):
        match = re.match(self.regex, code)
        if match:
            #print code
            #print "matched", self.regex
            literal_value = match.group(0)
            return ParseResult(literal_value, match)

class Or(object):
    def __init__(self, *args):
        self.items = args

    def parse(self, code):
        for parser in self.items:
            if type(parser) is str: # TODO we should have less if type()
                parser = grammar_or_regex(parser)
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
        ret = "ResultList(\n"
        for item in self.items:
            ret += indent(repr(item))
        ret += ")\n"
        return ret

class ZeroOrMore(object):
    def __init__(self, *args):
        self.item = Each(args)

    def parse(self, code):
        results = []
        while(True):
            result = self.item.parse(code)
            if result is None:
                return ResultList(results)
            code = code[result.matchlen:]
            results.extend(result) # TODO shouldn't this be append??

class OneOrMore(object):
    def __init__(self, *args):
        self.item = Each(args)

    def parse(self, code):
        result = Each(self.item, ZeroOrMore(self.item)).parse(code)
        if result is None:
            return None
        ret = []
        ret.append(result[0][0]) # TODO why do we need the zeroes here?
        for item in result[1]:
            ret.append(item[0][0]) # TODO why do we need the zeroes here?
        return ResultList(ret)

class ZeroOrOne(object):
    def __init__(self, *args):
        self.item = Each(args)

    def parse(self, code):
        if type(self.item) is str:
            self.item = grammar_or_regex(self.item)
        result = self.item.parse(code)
        if result is None:
            return ResultList([])
        # The each will make a ResultList, so we don't need to make another one.
        return result

class Each(object):
    def __init__(self, *args):
        self.items = args

    def parse(self, code):
        results = []
        for item in self.items:
            if type(item) is str:
                item = grammar_or_regex(item)
            if type(item) is list or type(item) is tuple:
                item = Each(*item)
            parse_result = item.parse(code)
            if parse_result is None:
                return None
            results.append(parse_result)
            code = code[parse_result.matchlen:]

        return ResultList(results)
    
    def __repr__(self):
        return "Each(" + repr(self.items) + ")"

def grammar_or_regex(name):
    from newlang import newlang_grammar, newlang_code # TODO grammar.py shouldn't depend on newlang anything
    if hasattr(newlang_code, name):
        return GrammarElement(name)
    else:
        # It's a regex, use the one already defined
        return getattr(newlang_grammar, name)

class GrammarElement(object):
    def __init__(self, name):
        self.name = name

    def defn(self):
        from newlang import newlang_grammar # TODO grammar.py shouldn't depend on newlang anything
        return getattr(newlang_grammar, self.name)

    def make_result(self, result):
        return GrammarElementResult(self.name, result)

    def parse(self, code):
        defn = self.defn()
        if type(defn) is list:
            defn = Each(*defn)
        result = defn.parse(code)
        if result is None:
            return None
        return self.make_result(result)

class GrammarElementResult(object):
    def __init__(self, name, result):
        self.name = name
        self.result = result
        self.matchlen = result.matchlen

    def tocode(self):
        from newlang import newlang_code # TODO grammar.py shouldn't depend on newlang anything
        return getattr(newlang_code, self.name)(self, self.result)

    def __repr__(self):
        return "GrammarElementResult(" + repr(self.name) + "," + repr(self.result) + ")"
