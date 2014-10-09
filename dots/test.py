import unittest2

class Dots(object):
    memo = {}

    def calculate(self, board, level=0):
        wins = False
        if board != [1]:
            for move in self.generateMoves(board):
                # If any one of our children is a loss, we're a win.
                # If all of our children are a win, we're a loss.
                if not self.wins(move, level+1):
                    # we can't just return here because we want to calculate all winning moves
                    wins = True
        return wins

    def wins(self, board, level=0):
        # Memoize the result
        rb = repr(board)
        if not rb in self.memo:
            result = self.calculate(board, level)
            self.memo[rb] = result

        # Get the memoized result
        result = self.memo[rb]

        if level <= 1 and not result:
                print board, "loses"
        if level == 0 and result:
                print board, "wins"
        return result

    def minimize(self, board):
        return board[0:board[0]]

    def generateMoves(self, board):
        for i in range(len(board)):
            r = list(board) # copy
            if r[i] > 0:
                s = r[i]
                for j in range(s-1, -1, -1):
                    r[i] = j
                    for x in range(i, len(r)):
                        if r[x] > j:
                            r[x] = j
                    if len(r) <= r[0] or r[r[0]] == 0:
                        m = self.minimize(r)
                        if len(m) > 0:
                            yield m

    def generateBoards(self):
        ret = [1]
        length = 1
        while True:
            yield ret
            ret = list(ret) # copy
            ret[length-1] += 1
            for i in range(length-1, 0, -1):
                if ret[i-1] < ret[i]:
                    ret[i] = 0
                    ret[i-1] += 1
            if ret[0] > length:
                ret = [0] * length
                length += 1
                ret.insert(0, length)


class TestDots(unittest2.TestCase):

    def setUp(self):
        self.sut = Dots()

    def tearDown(self):
        self.sut = None

    def testGenerateBoards(self):
        expected = [[1],
                    [2, 0],
                    [2, 1],
                    [2, 2],
                    [3, 0, 0],
                    [3, 1, 0],
                    [3, 1, 1],
                    [3, 2, 0],
                    [3, 2, 1],
                    [3, 2, 2],
                    [3, 3, 0],
                    [3, 3, 1],
                    [3, 3, 2],
                    [3, 3, 3],
                    [4, 0, 0, 0],
                    [4, 1, 0, 0],
                    [4, 1, 1, 0],
                   ]
        result = []
        generator = self.sut.generateBoards()
        for i in range(len(expected)):
            result.append(generator.next())

        self.assertEquals(expected, result)

    def testMinimize(self):
        self.assertEquals([1], self.sut.minimize([1, 0]))
        self.assertEquals([2, 0], self.sut.minimize([2, 0]))
        self.assertEquals([2, 0], self.sut.minimize([2, 0, 0]))

    def testGenerateMoves(self):
        # TODO: the order of these is really undefined...
        self.assertEquals([[1]], list(self.sut.generateMoves([2, 0])))
        self.assertEquals([[2, 0]], list(self.sut.generateMoves([2, 1])))
        self.assertEquals([[2, 1], [2, 0]], list(self.sut.generateMoves([2, 2])))
        self.assertEquals([[3, 2, 2], [3, 1, 1], [3, 0, 0], [3, 3, 2], [3, 3, 1], [3, 3, 0]], list(self.sut.generateMoves([3, 3, 3])))
        self.assertEquals([[2, 0], [1]], list(self.sut.generateMoves([3, 0, 0])))

    def testWinLoss(self):
        self.assertEquals(False, self.sut.wins([1]))
        self.assertEquals(True, self.sut.wins([2, 0]))
        self.assertEquals(False, self.sut.wins([2, 1]))
        self.assertEquals(True, self.sut.wins([2, 2]))
        self.assertEquals(True, self.sut.wins([3, 3, 3]))

if __name__ == "__main__":
    d = Dots()
    # We have to do these small-to-large because of the memoization.
    # TODO: auto-pad
    d.wins([3, 3, 0])
    d.wins([4, 4, 4, 0])
    d.wins([5, 5, 5, 5, 0])
    d.wins([6, 6, 6, 6, 6, 0])
    d.wins([7, 7, 7, 7, 7, 7, 0])
    d.wins([8, 8, 8, 8, 8, 8, 8, 0])
    d.wins([9, 9, 9, 9, 9, 9, 9, 9, 0])

    # for calculating everything (also remove prints above)
    # TODO: switches instead of comments?
    #for board in d.generateBoards():
    #    d.wins(board)
        #if d.wins(board):
        #    print board, "wins"
        #else:
        #    print board, "loses"
