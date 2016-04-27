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

class GameOfLifeBoard(object):
    def __init__(self):
        self.board = defaultdict(lambda: 0)

    def turnOnCell(self, cell):
        self.board[cell] = ALIVE
        self.getNeighborCount(cell)  # Touch cells around it so they get calculated later

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

    def shouldProcessCells(self):
        return self.board.keys()

    def getCell(self, cell):
        return self.board[cell] == ALIVE

    def calculate_next_generation(self, cell):
        return process(self.getNeighborCount(cell), self.getCell(cell))

class GameOfLife(object):
    def __init__(self):
        self.board = GameOfLifeBoard()

    def turnOnCell(self, cell):
        self.board.turnOnCell(cell)

    def getCell(self, cell):
        return self.board.getCell(cell)

    def tick(self):
        newboard = GameOfLifeBoard()
        for cell in self.board.shouldProcessCells():
            if self.board.calculate_next_generation(cell) == ALIVE:
                newboard.turnOnCell(cell)
        self.board = newboard

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

class TestGameOfLife(unittest.TestCase):

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
        sut = GameOfLifeBoard()
        sut.turnOnCell((10, 10))
        sut.turnOnCell((11, 10))
        self.assertEquals(1, sut.getNeighborCount((10, 10)))
        self.assertEquals(1, sut.getNeighborCount((11, 10)))
        self.assertEquals(2, sut.getNeighborCount((10, 11)))

    def test_11_1(self): # to be different from test_cell_neighbors
        sut = GameOfLifeBoard()
        sut.turnOnCell((10, 10))
        self.assertEquals(1, sut.getNeighborCount((10, 11)))

    def test_all_neighbors(self):
        sut = GameOfLifeBoard()
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
