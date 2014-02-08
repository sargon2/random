import unittest2

# Players take turns.
# When it's a player's turn, he places a symbol on the board at a specific (unused) location.
# If a player gets a line of symbols from one edge to the opposite edge (either straight or diagonally), they win.
# If there are no spots left on the board, the game is a draw.

class Player(object):
    pass

class TurnManager(object):
    def __init__(self, *args):
        prev_player = self.current_player = args[len(args)-1]
        for player in args:
            prev_player.next_player = prev_player = player

    def whoseTurnIsIt(self):
        self.current_player = self.current_player.next_player
        return self.current_player


class Board(object):
    def __init__(self, width, height):
        self.size = (width, height)
        self.pieces = {}

    def move(self, x, y, symbol):
        self.pieces[(x, y)] = symbol

    def get(self, x, y):
        return self.pieces[(x, y)]


class TestBoard(unittest2.TestCase):
    def test_board_construct(self):
        self.assertEquals((2, 2), Board(2, 2).size)
        self.assertEquals((2, 3), Board(2, 3).size)

    def test_make_move(self):
        b = Board(3, 3)
        b.move(0, 0, 'x')
        self.assertEquals('x', b.get(0, 0))

    def test_make_move_different(self):
        b = Board(3, 3)
        b.move(0, 1, 'o')
        self.assertEquals('o', b.get(0, 1))


class TestTurnManager(unittest2.TestCase):
    def test_single_player_turn(self):
        p = Player()
        t = TurnManager(p)
        self.assertEquals(p, t.whoseTurnIsIt())
        self.assertEquals(p, t.whoseTurnIsIt())

    def test_two_player_turn(self):
        p1 = Player()
        p2 = Player()
        t = TurnManager(p1, p2)
        self.assertEquals(p1, t.whoseTurnIsIt())
        self.assertEquals(p2, t.whoseTurnIsIt())
        self.assertEquals(p1, t.whoseTurnIsIt())
        self.assertEquals(p2, t.whoseTurnIsIt())

    def test_three_player_turn(self):
        p1 = Player()
        p2 = Player()
        p3 = Player()
        t = TurnManager(p1, p2, p3)
        self.assertEquals(p1, t.whoseTurnIsIt())
        self.assertEquals(p2, t.whoseTurnIsIt())
        self.assertEquals(p3, t.whoseTurnIsIt())
        self.assertEquals(p1, t.whoseTurnIsIt())
        self.assertEquals(p2, t.whoseTurnIsIt())
        self.assertEquals(p3, t.whoseTurnIsIt())
