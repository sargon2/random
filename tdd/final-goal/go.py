import unittest2


class App(object):
    pass

class Game(App):
    pass


class TestGame(unittest2.TestCase):
    def isProfitable(self, app):
        pass

    def getGoodGame(self):
        return Game()

    def getBadGame(self):
        return Game()

    def getBadApp(self):
        return App()

    def assertGameIsFun(self, game):
        pass

    def assertAppIsProfitable(self, app):
        self.assertTrue(self.isProfitable(app))

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
