
import unittest
from SimpleGame import SimpleGame


class TestSimpleGame(unittest.TestCase):
    def setUp(self):
        # Testing the setup in a simple game
        self.game = SimpleGame(3)
        self.game.blue_player.set_letter("S")
        self.game.red_player.set_letter("O")

    def test_win_condition_horizontal(self):
        # Tests that the game ends immediately on the first horizontal SOS.
        game = self.game
        game.make_move(0, 0, "S")
        game.make_move(1, 0, "O")
        game.make_move(0, 1, "O")
        game.make_move(1, 1, "S")
        game.make_move(0, 2, "S")

        self.assertTrue(game.is_game_over())
        self.assertEqual(game.get_winner(), "Blue")
        self.assertEqual(game.blue_player.score, 1)
        self.assertEqual(game.current_turn.color, "Blue")  # Blue retains turn

    def test_draw_condition_3x3(self):
        # Tests that the game ends in a draw if the board is full and no SOS is made.
        game = self.game
        # Moves to fill board without forming SOS
        moves = [
            (0, 0, "S"), (0, 1, "O"), (0, 2, "S"),
            (1, 0, "O"), (1, 1, "S"), (1, 2, "O"),
            (2, 0, "S"), (2, 1, "O"), (2, 2, "S")
        ]

        for r, c, l in moves:
            # Player letter is driven by the game's current turn
            player_letter = self.game.current_turn.letter_choice
            self.game.make_move(r, c, player_letter)

        self.assertTrue(game.is_game_over())
        self.assertEqual(game.get_winner(), "Draw")
        self.assertEqual(game.blue_player.score, 0)
        self.assertTrue(game.board.is_full())