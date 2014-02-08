import unittest

# https://sites.google.com/site/tddproblems/all-problems-1/game-of-life
DEAD = False
ALIVE = True

class TestThings(unittest.TestCase):

    def process(self, num_neighbors, is_alive):
        if num_neighbors == 3:
            return ALIVE
        if num_neighbors == 2 and is_alive == ALIVE:
            return ALIVE
        return DEAD

    def assert_state(self, is_alive, num_neighbors, expected_result):
        result = self.process(num_neighbors, is_alive)
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
