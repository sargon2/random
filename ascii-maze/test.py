import unittest2
import operator

# Pick a random spot that's not on an edge
# Continue to move in random directions, avoiding connecting to empty spots or edges, until trapped
# Pick another random spot that's already been cleared, repeat

# Operations:
# position = clear_and_move(position, direction)
# get_movable_directions(position)
# get_startable_positions()

class Directions:
    right = (1, 0)
    left = (-1, 0)
    up = (0, -1)
    down = (0, 1)
    all = [left, right, up, down]

class InvalidArgumentException(Exception):
    pass

class MazeTest(unittest2.TestCase):
    def test_constructor(self):
        Maze(3, 3)

    def assertValidSize(self, width, height):
        Maze(width, height)

    def assertInvalidSize(self, width, height):
        with self.assertRaises(InvalidArgumentException):
            Maze(width, height)

    def test_valid_sizes(self):
        # invalid

        ##
        ## invalid

        ###
        # #
        ### valid

        ####
        ####
        #  #
        #### invalid!

        #####
        #   #
        ### #
        #   #
        ##### valid

        # Mazes must be odd by odd.  1xn and nx1 are invalid.
        self.assertValidSize(3, 3)
        self.assertValidSize(5, 5)
        self.assertValidSize(3, 5)
        self.assertValidSize(3, 17)

        self.assertInvalidSize(-1, -1)
        self.assertInvalidSize(-1, 3)
        self.assertInvalidSize(3, -1)
        self.assertInvalidSize(1, 0)
        self.assertInvalidSize(0, 1)
        self.assertInvalidSize(1, 1)

        self.assertInvalidSize(2, 1)
        self.assertInvalidSize(1, 2)
        self.assertInvalidSize(2, 2)

        self.assertInvalidSize(4, 3)
        self.assertInvalidSize(3, 4)
        self.assertInvalidSize(4, 4)

        self.assertInvalidSize(9, 14)

    def test_get_startable_positions_3_3(self):
        m = Maze(3, 3)
        s = m.getStartablePositions()
        self.assertEquals(1, len(s))
        self.assertEquals((1, 1), s[0])

    def test_get_startable_positions_5_3(self):
        m = Maze(5, 3)
        s = m.getStartablePositions()
        self.assertEquals(2, len(s))
        self.assertEquals((1, 1), s[0])
        self.assertEquals((3, 1), s[1])

    def test_clear_and_move(self):
        m = Maze(5, 3)
        m.clearAndMove((1, 1), Directions.right)
        self.assertEquals([[True, True, True, True, True],
                           [True, False, False, False, True],
                           [True, True, True, True, True]], m.getMaze())

    def test_clear_and_move_left(self):
        m = Maze(5, 3)
        m.clearAndMove((3, 1), Directions.left)
        self.assertEquals([[True, True, True, True, True],
                           [True, False, False, False, True],
                           [True, True, True, True, True]], m.getMaze())

    def test_clear_and_move_down(self):
        m = Maze(3, 5)
        m.clearAndMove((1, 1), Directions.down)
        self.assertEquals([[True, True, True],
                           [True, False, True],
                           [True, False, True],
                           [True, False, True],
                           [True, True, True]], m.getMaze())

    def test_clear_and_move_up(self):
        m = Maze(3, 5)
        m.clearAndMove((1, 3), Directions.up)
        self.assertEquals([[True, True, True],
                           [True, False, True],
                           [True, False, True],
                           [True, False, True],
                           [True, True, True]], m.getMaze())

    def test_get_maze(self):
        # Note that these duplicate pointers.
        self.assertEquals([[True] * 3] * 3, Maze(3, 3).getMaze())
        self.assertEquals([[True] * 5] * 3, Maze(5, 3).getMaze())

    def test_get_startable_positions_one_empty(self):
        m = Maze(7, 3)
        m.clearAndMove((1, 1), Directions.right)
        s = m.getStartablePositions()
        self.assertEquals(1, len(s))
        self.assertEquals((3, 1), s[0])

    def test_get_movable_directions(self):
        m = Maze(5, 3)
        dirs = m.getMovableDirections((1, 1))
        self.assertEquals(1, len(dirs))
        self.assertEquals((1, 0), dirs[0])


class Maze(object):

    def __init__(self, width, height):
        if width < 3 or height < 3 or (height*width) % 2 == 0:
            raise InvalidArgumentException()
        self.width = width
        self.height = height
        self.maze = [[True for i in range(width)] for i in range(height)]
        self.isEmpty = True

    def getMaze(self):
        return self.maze

    def get(self, position):
        return self.maze[position[1]][position[0]] # note swapped

    def getMovableDirections(self, position):
        ret = []
        for direction in Directions.all:
            p2 = position
            for i in range(2):
                p2 = self.move(p2, direction)
            if self.isInRange(p2):
                if self.get(p2):
                    ret.append(direction)
        return ret

    def hasNearbyUncarved(self, position):
        return len(self.getMovableDirections(position)) > 0

    def isInRange(self, position):
        (x, y) = position
        return y > 0 and x > 0 and y < self.height-1 and x < self.width-1

    def getStartablePositions(self):
        ret = []
        for i in range(1, self.width-1, 2):
            for j in range(1, self.height-1, 2):
                position = (i, j)
                if self.isEmpty:
                    ret.append(position)
                else:
                    if not self.get(position): # We can only start on an existing path.
                        if self.hasNearbyUncarved(position):
                            ret.append(position)
        return ret

    def carve(self, position):
        self.isEmpty = False
        self.maze[position[1]][position[0]] = False

    def clearAndMove(self, position, direction):
        self.carve(position)
        for i in range(2):
            position = self.clearAndMoveOne(position, direction)
        return position

    def clearAndMoveOne(self, position, direction):
        position = self.move(position, direction)
        self.carve(position)
        return position

    def move(self, position, direction):
        return tuple(map(operator.add, position, direction))
