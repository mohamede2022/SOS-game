import unittest
from player import Player

class TestPlayer(unittest.TestCase):
    def test_player_choice(self):
        player = Player("Blue")
        player.choose_letter("S")
        self.assertEqual(player.current_letter, "S")
        self.assertEqual(player.color, "Blue")

if __name__ == "__main__":
    unittest.main()
