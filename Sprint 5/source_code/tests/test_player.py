
import unittest
from player import Player


class TestPlayer(unittest.TestCase):
    def test_player_choice(self):
        player = Player("Blue")
        player.set_letter("S")
        self.assertEqual(player.letter_choice, "S")
        self.assertEqual(player.color, "Blue")

    def test_player_score_initialization(self):
        # Tests that a player starts with a score of 0.
        player = Player("Red")
        self.assertEqual(player.score, 0)


if __name__ == "__main__":
    unittest.main()