# problem 5 here: https://blog.svpino.com/2015/05/07/five-programming-problems-every-software-engineer-should-be-able-to-solve-in-less-than-1-hour

# TDD?
# I don't know how many answers there are.  How do I convince myself it's correct?
# It can evaluate the strings produced by the generator to ensure they really add up to 100.

import unittest2

def get_results():
    return tryone("", 0)

def tryone(currstr, pos):
    if pos > 8:
        if eval(currstr) == 100:
            return [currstr]
        else:
            return []
    pos += 1
    results = []
    results.extend(tryone(currstr + "" + str(pos), pos))
    if pos > 1:
        results.extend(tryone(currstr + "+" + str(pos), pos))
    results.extend(tryone(currstr + "-" + str(pos), pos))
    return results


class TestSomething(unittest2.TestCase):
    def evaluate(self, result):
        return eval(result)
    def strip_other(self, result):
        return result.replace("+", "").replace("-", "")
    def test_something(self):
        count = 0
        for result in get_results():
            count += 1
            self.assertEquals(100, self.evaluate(result))
            self.assertEquals("123456789", self.strip_other(result))
        self.assertGreater(count, 5) # there are at least 5 solutions

if __name__ == "__main__":
    results = get_results()
    for result in results:
        print result
