import unittest2


class App(object):
    pass

class Game(App):
    pass


class TestGame(unittest2.TestCase):
    def getGoodGame(self):
        return Game()

    def getBadGame(self):
        return Game()

    def getBadApp(self):
        return App()

    def assertGameIsFun(self, game):
        self.assertHasPleasingColorScheme(game)
        self.assertIsJuicy(game)
        # what else? assert that it has addictive elements?
        # assert when the user runs it, it might go better the following time they run it?

    def assertAppIsProfitable(self, app):
        self.assertHasMechanismToCollectMoney(app)
        self.assertIsPopular(app)
        # now what? assert a certain % of users provide money?
        # assert it's been used to collect at least $x?
        # assert that it's been used to collect at least $x in the last y time?

    def test_game_is_successful(self):
        game = self.getGoodGame()
        self.assertGameIsFun(game)
        self.assertAppIsProfitable(game)

    def test_game_is_not_fun(self):
        game = self.getBadGame()
        with self.assertRaises(AssertionError):
            self.assertGameIsFun(game)

    def test_app_is_not_profitable(self):
        app = self.getBadApp()
        with self.assertRaises(AssertionError):
            self.assertAppIsProfitable(app)
