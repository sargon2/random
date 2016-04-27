import unittest2

# from https://oeis.org/A000002
first_few = [1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 2]

def generate_kolakoski():
    working = [1, 2, 2]
    yield 1
    yield 2
    yield 2
    pos = 2
    curr = 1
    while True:
        for i in range(0, working[pos]):
            working.append(curr)
            yield curr
        curr = 3 - curr
        pos += 1


def generate_kolakoski_n_(n):
    # If you can implement this function without using a loop, you win $200:
    # http://faculty.evansville.edu/ck6/integer/unsolved.html
    if n in [1, 4, 5, 7, 10, 13, 14, 16, 17, 20]: # https://oeis.org/A013947
        return 1
    return 2

def generate_kolakoski_n(n):
    generator = generate_kolakoski()
    for i in range(0, n):
        ret = generator.next()
    return ret

class TestKolakoski(unittest2.TestCase):
    def test_generator(self):
        for x, y in zip(generate_kolakoski(), first_few):
            self.assertEquals(x, y)

    def test_n(self):
        for i in range(0, len(first_few)):
            self.assertEquals(generate_kolakoski_n(i + 1), first_few[i], "seqnum is " + str(i+1))
