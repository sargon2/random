import unittest2
from collections import deque

# http://gojko.net/2009/08/02/tdd-as-if-you-meant-it-revisited/

# (done) a game is over when all fields are taken
# (done) a game is over when all fields in a column are taken by a player
# (skipped, trivial) a game is over when all fields in a row are taken by a player
# (skipped, trivial) a game is over when all fields in a diagonal are taken by a player
# (done) a player can take a field if not already taken
# (done) players take turns taking fields until the game is over

# Requirements added by me that weren't part of the original set:
#
# (skipped, trivial) a single field can be in all 3 of a row, column, and diagonal
# (skipped, trivial) a tic-tac-toe board consists of fields arranged into rows, columns, and diagonals
# (done) a player wins the game when he or she takes all the fields in any one row, column, or diagonal

# Notes (todo?):
# There's duplication between the player owning a field and the field knowing it's taken.
#   The setGame method on player makes it too mutable.
# There's some weirdness with the dependency graph.
#   Game knows it has players, and players know they're in a game.
#   Individual fields know their game, but the fields class doesn't.

class Game(object):
    def __init__(self):
        self.players = deque()
        self.fields = []

    def addPlayers(self, *players):
        for player in players:
            self.players.append(player)
            player.setGame(self)

    def addFields(self, *fields):
        for fieldset in fields:
            self.fields.append(fieldset)

    def whoseTurnIsIt(self):
        return self.players[0]

    def isGameOver(self):
        for fields in self.fields:
            if fields.isGameOver():
                return True
        return False

    def advance(self):
        self.players.rotate()

    def getWinner(self):
        for player in self.players:
            for fields in self.fields:
                if player.ownsAll(fields):
                    return player
        return None

class Field(object):
    def __init__(self, game = None):
        self.taken = False
        self.game = game

    def take(self):
        if self.taken:
            raise Exception("Field already taken")
        self.taken = True
        self.game.advance()

    def isTaken(self):
        return self.taken

class Fields(object):
    def __init__(self, *fields):
        self.fields = []
        for field in fields:
            self.add(field)

    def add(self, field):
        self.fields.append(field)

    def isGameOver(self):
        for field in self.fields:
            if not field.isTaken():
                return False
        return True

class Player(object):
    def __init__(self):
        self.fields = []

    def setGame(self, game):
        self.game = game

    def take(self, field):
        if self.game.whoseTurnIsIt() != self:
            raise Exception("Move out of turn")
        field.take()
        self.fields.append(field)

    def ownsAll(self, fields):
        for field in fields.fields:
            if not field in self.fields:
                return False
        return True


class TestTicTacToe(unittest2.TestCase):
    def test_field_exists(self):
        Field()

    def test_fields_exist(self):
        Fields()

    def test_fields_can_be_taken(self):
        Field(Game()).take()

    def test_game_is_over_when_no_fields(self):
        fields = Fields()
        self.assertTrue(fields.isGameOver())

    def test_game_is_over_when_all_fields_taken(self):
        g = Game()
        fields = Fields()
        f = Field(g)
        fields.add(f)
        self.assertFalse(fields.isGameOver())
        f.take()
        self.assertTrue(fields.isGameOver())

    def test_game_is_over_when_all_fields_in_column_taken_by_player(self):
        g = Game()
        player = Player()
        g.addPlayers(player)
        column = Fields()
        f = Field(g)
        column.add(f)
        self.assertFalse(column.isGameOver())
        player.take(f)  # taken *by player*
        self.assertTrue(column.isGameOver())

    def test_player_cannot_take_already_taken_field(self):
        g = Game()
        f = Field(g)
        p = Player()
        g.addPlayers(p)
        p.take(f)
        with self.assertRaises(Exception):
            p.take(f)

    def test_players_take_turns_taking_fields_until_game_is_over(self):
        game = Game()
        p1 = Player()
        p2 = Player()

        game.addPlayers(p1, p2)
        fields = Fields()
        f1 = Field(game)
        f2 = Field(game)
        f3 = Field(game)
        fields.add(f1)
        fields.add(f2)
        fields.add(f3)
        game.addFields(fields)

        self.assertEquals(p1, game.whoseTurnIsIt())
        self.assertEquals(p1, game.whoseTurnIsIt())
        self.assertFalse(game.isGameOver())
        self.assertEquals(None, game.getWinner())

        p1.take(f1)

        self.assertEquals(p2, game.whoseTurnIsIt())
        self.assertFalse(game.isGameOver())
        self.assertEquals(None, game.getWinner())

        p2.take(f2)

        self.assertEquals(p1, game.whoseTurnIsIt())
        self.assertFalse(game.isGameOver())
        self.assertEquals(None, game.getWinner())

        p1.take(f3)

        self.assertEquals(p2, game.whoseTurnIsIt())
        self.assertTrue(game.isGameOver())
        self.assertEquals(None, game.getWinner())

    def test_normal_board_arrangement(self):
        game = Game()
        upperleft = Field(game)
        uppermiddle = Field(game)
        upperright = Field(game)
        middleleft = Field(game)
        middlemiddle = Field(game)
        middleright = Field(game)
        lowerleft = Field(game)
        lowermiddle = Field(game)
        lowerright = Field(game)

        row1 = Fields(upperleft, uppermiddle, upperright)
        row2 = Fields(middleleft, middlemiddle, middleright)
        row3 = Fields(lowerleft, lowermiddle, lowerright)

        col1 = Fields(upperleft, middleleft, lowerleft)
        col2 = Fields(uppermiddle, middlemiddle, lowermiddle)
        col3 = Fields(upperright, middleright, lowerright)

        diag1 = Fields(upperleft, middlemiddle, lowerright)
        diag2 = Fields(lowerleft, middlemiddle, upperright)

        game.addFields(row1, row2, row3)
        game.addFields(col1, col2, col3)
        game.addFields(diag1, diag2)

        # What asserts?  No asserts to make here.  The board arrangement is configuration, not code.

    def test_error_if_player_goes_out_of_turn(self):
        game = Game()
        p1 = Player()
        p2 = Player()
        game.addPlayers(p1, p2)

        f1 = Field(game)
        f2 = Field(game)
        f3 = Field(game)
        fields = Fields(f1, f2, f3)

        game.addFields(fields)

        p1.take(f1)
        with self.assertRaises(Exception):
            p1.take(f2)

    def test_winner(self):
        game = Game()
        p1 = Player()
        p2 = Player()
        game.addPlayers(p1, p2)

        f1 = Field(game)
        f2 = Field(game)
        f3 = Field(game)
        f4 = Field(game)
        f5 = Field(game)

        fields1 = Fields(f1, f2, f3)
        fields2 = Fields(f1, f4, f5)
        game.addFields(fields1, fields2)

        self.assertEquals(None, game.getWinner())

        p1.take(f1)
        p2.take(f4)
        p1.take(f2)
        p2.take(f5)
        p1.take(f3)

        self.assertTrue(game.isGameOver())
        self.assertEquals(p1, game.getWinner())
