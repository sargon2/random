import unittest2

# Pick a random spot that's not on an edge
# Continue to move in random directions, avoiding connecting to empty spots or edges, until trapped
# Pick another random spot that's already been cleared, repeat

# Operations:
# position = clear_and_move(position, direction)
# get_movable_directions(position)
# get_startable_positions()

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

    def test_get_startable_positions_one_empty(self):
        self.fail("Not written yet")

    def test_clear_and_move(self):
        self.fail("Not written yet")


class Maze(object):

    def __init__(self, width, height):
        if width < 3 or height < 3 or width % 2 == 0 or height % 2 == 0:
            raise InvalidArgumentException()
        self.width = width
        self.height = height

    def getStartablePositions(self):
        ret = []
        for i in range(1, self.width-1, 2):
            for j in range(1, self.height-1, 2):
                ret.append((i, j))
        return ret
