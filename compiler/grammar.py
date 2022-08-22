import re

class ParseError(Exception):
    pass

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

    def parse(self, code, language_provider):
        if code == '':
            return self
        return None

class Regex(object):
    def __init__(self, regex):
        self.regex = regex

    def parse(self, code, language_provider):
        match = re.match(self.regex, code)
        if match:
            #print("regex matched", self.regex, "in", repr(code))
            literal_value = match.group(0)
            return ParseResult(literal_value, match)

class Or(object):
    def __init__(self, *args):
        self.items = args

    def parse(self, code, language_provider):
        for parser in self.items:
            if type(parser) is str: # TODO we should have less if type()
                parser = grammar_or_regex(parser, language_provider)
            if type(parser) is list or type(parser) is tuple:
                parser = Each(*parser)
            parse_result = parser.parse(code, language_provider)
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
        self.item = Each(*args)

    def parse(self, code, language_provider):
        results = []
        while(True):
            result = self.item.parse(code, language_provider)
            if result is None:
                return ResultList(results)
            code = code[result.matchlen:]
            results.append(result)

class OneOrMore(object):
    def __init__(self, *items):
        self.items = items

    def parse(self, code, language_provider):
        result = Each(self.items, ZeroOrMore(self.items)).parse(code, language_provider)
        if result is None:
            return None
        ret = []
        # Zero is needed here because our outer Each always has its first iteration in the 0th position.
        # It's specified above.
        ret.append(result[0])
        for item in result[1]:
            # Zero is needed here because ZeroOrMore always returns a list of groups. 
            # Our group always has one item because there's only one specified above.
            ret.append(item[0])
        return ResultList(ret)

class ZeroOrOne(object):
    def __init__(self, *args):
        self.item = Each(*args)

    def parse(self, code, language_provider):
        if type(self.item) is str:
            self.item = grammar_or_regex(self.item, language_provider)
        result = self.item.parse(code, language_provider)
        if result is None:
            return ResultList([])
        # The each will make a ResultList, so we don't need to make another one.
        return result

class Each(object):
    def __init__(self, *args):
        self.items = args

    def parse(self, code, language_provider):
        results = []
        for item in self.items:
            if type(item) is str:
                item = grammar_or_regex(item, language_provider)
            if type(item) is list or type(item) is tuple:
                item = Each(*item)
            parse_result = item.parse(code, language_provider)
            if parse_result is None:
                return None
            results.append(parse_result)
            code = code[parse_result.matchlen:]

        return ResultList(results)
    
    def __repr__(self):
        return "Each(" + repr(self.items) + ")"

def grammar_or_regex(name, language_provider): # TODO should this move to the provider?
    if language_provider.has_code_for(name):
        return GrammarElement(name)
    else:
        # It's a regex, use the one already defined
        return language_provider.get_grammar(name)

class GrammarElement(object):
    def __init__(self, name):
        self.name = name

    def parse(self, code, language_provider):
        defn = language_provider.get_grammar(self.name)
        if type(defn) is list:
            defn = Each(*defn)
        result = defn.parse(code, language_provider)
        if result is None:
            #print("Failed to parse", repr(code), "as", self.name)
            return None
        #else:
        #    print("Parsed", repr(code), "as", self.name)
        return GrammarElementResult(self.name, result, language_provider)

class GrammarElementResult(object):
    def __init__(self, name, result, code_provider):
        self.name = name
        self.result = result
        self.matchlen = result.matchlen
        self.code_provider = code_provider

    def tocode(self):
        return self.code_provider.get_code(self.name, self.result)

    def __repr__(self):
        return "GrammarElementResult(" + repr(self.name) + "," + repr(self.result) + ")"
