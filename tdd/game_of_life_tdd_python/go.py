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
        return defaultdict(lambda: 0)

    def __init__(self):
        self.board = self.make_board()

    def turnOnCell(self, cell):
        self.board[cell] = ALIVE

    def getNeighborCount(self, cell):
        x, y = cell
        # I tried this with loops, but it's faster to unroll them.
        return self.board[(x+1, y)] \
             + self.board[(x-1, y)] \
             + self.board[(x, y+1)] \
             + self.board[(x, y-1)] \
             + self.board[(x+1, y+1)] \
             + self.board[(x+1, y-1)] \
             + self.board[(x-1, y+1)] \
             + self.board[(x-1, y-1)]

    def touchNearbyCells(self):
        # Touch cells near cells that are turned on so they get calculated later.
        for cell in self.board.keys():
            self.getNeighborCount(cell)

    def tick(self):
        self.touchNearbyCells()
        newboard = self.make_board()
        for cell in self.board.keys():
            # We don't want to set dead cells because we don't want to calculate them unnecessarily.
            if process(self.getNeighborCount(cell), self.board[cell]) == ALIVE:
                newboard[cell] = ALIVE
        self.board = newboard

    def getCell(self, cell):
        return self.board[cell] == ALIVE

    def runAndRender(self): # TODO: untested
        import time
        while True:
            for y in range(-10, 10):
                for x in range(-10, 10):
                    if self.getCell((x, y)):
                        print "#",
                    else:
                        print " ",
                print
            self.tick()
            time.sleep(0.5)

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
        sut.turnOnCell((10, 10))
        sut.turnOnCell((11, 10))
        self.assertEquals(1, sut.getNeighborCount((10, 10)))
        self.assertEquals(1, sut.getNeighborCount((11, 10)))
        self.assertEquals(2, sut.getNeighborCount((10, 11)))

    def test_11_1(self): # to be different from test_cell_neighbors
        sut = GameOfLife()
        sut.turnOnCell((10, 10))
        self.assertEquals(1, sut.getNeighborCount((10, 11)))

    def test_all_neighbors(self):
        sut = GameOfLife()
        for x in range(20, 23):
            for y in range(30, 33):
                sut.turnOnCell((x, y))
        self.assertEquals(8, sut.getNeighborCount((21, 31)))
        self.assertEquals(5, sut.getNeighborCount((20, 31)))
        self.assertEquals(5, sut.getNeighborCount((22, 31)))

    def assertDies(self, sut, cell):
        self.assertTrue(sut.getCell(cell))
        sut.tick()
        self.assertFalse(sut.getCell(cell))

    def assertAnimates(self, sut, cell):
        self.assertFalse(sut.getCell(cell))
        sut.tick()
        self.assertTrue(sut.getCell(cell))

    def test_advance_state(self):
        sut = GameOfLife()
        sut.turnOnCell((10, 10))
        self.assertDies(sut, (10, 10))

    def test_advance_state_different(self):
        sut = GameOfLife()
        sut.turnOnCell((11, 11))
        self.assertDies(sut, (11, 11))

    def test_advance_state_on(self):
        sut = GameOfLife()
        sut.turnOnCell((9, 9))
        sut.turnOnCell((10, 9))
        sut.turnOnCell((11, 9))
        self.assertAnimates(sut, (10, 10))

    def test_advance_state_on_different(self):
        sut = GameOfLife()
        sut.turnOnCell((10, 10))
        sut.turnOnCell((11, 10))
        sut.turnOnCell((12, 10))
        self.assertAnimates(sut, (11, 11))

    def test_advance_state_on_different2(self):
        sut = GameOfLife()
        sut.turnOnCell((10, 10))
        sut.turnOnCell((11, 10))
        sut.turnOnCell((12, 10))
        self.assertAnimates(sut, (11, 9))

    def test_dict_out_of_order(self):
        sut = GameOfLife()
        sut.turnOnCell((0, 1))
        sut.turnOnCell((0, 2))
        sut.turnOnCell((0, 3))
        # It's important that we not call getCell on it before tick().
        sut.tick()
        self.assertTrue(sut.getCell((-1, 2)))

    def test_dict_out_of_order_after_two(self):
        sut = GameOfLife()
        sut.turnOnCell((-1, 2))
        sut.turnOnCell((0, 2))
        sut.turnOnCell((1, 2))
        # It's important that we not call getCell on it before tick().
        sut.tick()
        sut.tick()
        self.assertTrue(sut.getCell((-1, 2)))

def main(): # TODO: untested
    game = GameOfLife()
    game.turnOnCell((1, 1))
    game.turnOnCell((1, 3))

    game.turnOnCell((0, 1))
    game.turnOnCell((0, 2))
    game.turnOnCell((0, 3))

    game.turnOnCell((2, 1))
    game.turnOnCell((2, 2))
    game.turnOnCell((2, 3))
    game.runAndRender()

if __name__ == "__main__":
    main()
