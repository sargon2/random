import unittest
from collections import defaultdict

# https://sites.google.com/site/tddproblems/all-problems-1/game-of-life
DEAD = 0
ALIVE = 1

def process(num_neighbors, is_alive):
    if num_neighbors == 3:
        return ALIVE
    if num_neighbors == 2 and is_alive == ALIVE:
        return ALIVE
    return DEAD

class GameOfLife(object):
    def make_board(self):
        return defaultdict(lambda: defaultdict(lambda: 0))

    def __init__(self):
        self.board = self.make_board()

    def turnOnCell(self, x, y):
        self.board[x][y] = ALIVE

    def getNeighborCount(self, x, y):
        # I tried this with loops, but it's faster to unroll them.
        return self.board[x+1][y] \
             + self.board[x-1][y] \
             + self.board[x][y+1] \
             + self.board[x][y-1] \
             + self.board[x+1][y+1] \
             + self.board[x+1][y-1] \
             + self.board[x-1][y+1] \
             + self.board[x-1][y-1]

    def tick(self):
        newboard = self.make_board()
        for (rowkey, row) in self.board.items():
            for (cellkey, cell) in row.items():
                print "processing", rowkey, cellkey
                newboard[rowkey][cellkey] = process(self.getNeighborCount(rowkey, cellkey), cell)
        self.board = newboard

    def getCell(self, x, y):
        return self.board[x][y] == ALIVE

class TestThings(unittest.TestCase):

    def assert_state(self, is_alive, num_neighbors, expected_result):
        result = process(num_neighbors, is_alive)
        self.assertEquals(result, expected_result)

    def assert_neighbor_state_change(self, num_neighbors, if_was_alive, if_was_dead):
        self.assert_state(True, num_neighbors, if_was_alive)
        self.assert_state(False, num_neighbors, if_was_dead)

    def test_rules(self):
        self.assert_neighbor_state_change(0, DEAD, DEAD)
        self.assert_neighbor_state_change(1, DEAD, DEAD)
        self.assert_neighbor_state_change(2, ALIVE, DEAD)
        self.assert_neighbor_state_change(3, ALIVE, ALIVE)
        self.assert_neighbor_state_change(4, DEAD, DEAD)
        self.assert_neighbor_state_change(5, DEAD, DEAD)
        self.assert_neighbor_state_change(6, DEAD, DEAD)
        self.assert_neighbor_state_change(7, DEAD, DEAD)
        self.assert_neighbor_state_change(8, DEAD, DEAD)

    def test_cell_neighbors(self):
        sut = GameOfLife()
        sut.turnOnCell(10, 10)
        sut.turnOnCell(11, 10)
        self.assertEquals(1, sut.getNeighborCount(10, 10))
        self.assertEquals(1, sut.getNeighborCount(11, 10))
        self.assertEquals(2, sut.getNeighborCount(10, 11))

    def test_11_1(self): # to be different from test_cell_neighbors
        sut = GameOfLife()
        sut.turnOnCell(10, 10)
        self.assertEquals(1, sut.getNeighborCount(10, 11))

    def test_all_neighbors(self):
        sut = GameOfLife()
        for x in range(20, 23):
            for y in range(30, 33):
                sut.turnOnCell(x, y)
        self.assertEquals(8, sut.getNeighborCount(21, 31))
        self.assertEquals(5, sut.getNeighborCount(20, 31))
        self.assertEquals(5, sut.getNeighborCount(22, 31))

    def assertDies(self, sut, x, y):
        self.assertTrue(sut.getCell(x, y))
        sut.tick()
        self.assertFalse(sut.getCell(x, y))

    def assertAnimates(self, sut, x, y):
        self.assertFalse(sut.getCell(x, y))
        sut.tick()
        self.assertTrue(sut.getCell(x, y))

    def test_advance_state(self):
        sut = GameOfLife()
        sut.turnOnCell(10, 10)
        self.assertDies(sut, 10, 10)

    def test_advance_state_different(self):
        sut = GameOfLife()
        sut.turnOnCell(11, 11)
        self.assertDies(sut, 11, 11)

    def test_advance_state_on(self):
        sut = GameOfLife()
        sut.turnOnCell(9, 9)
        sut.turnOnCell(10, 9)
        sut.turnOnCell(11, 9)
        self.assertAnimates(sut, 10, 10)

    def test_advance_state_on_different(self):
        sut = GameOfLife()
        sut.turnOnCell(10, 10)
        sut.turnOnCell(11, 10)
        sut.turnOnCell(12, 10)
        self.assertAnimates(sut, 11, 11)
