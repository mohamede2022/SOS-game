
import unittest
from GeneralGame import GeneralGame


class TestGeneralGame(unittest.TestCase):

    def test_multiple_sos_scoring_and_turn_retain(self):
        #Tests that a player scores, retains their turn, and continues the game.
        game = GeneralGame(4)
        game.blue_player.set_letter("S")
        game.red_player.set_letter("O")

        # Blue's turn
        game.make_move(1, 0, "S")  # Blue (1,0) - No score. Turn toggles to Red
        self.assertEqual(game.current_turn.color, "Red")

        # Red's turn
        game.make_move(1, 1, "O")  # Red (1,1) - No score. Turn toggles to Blue
        self.assertEqual(game.current_turn.color, "Blue")

        # Blue's turn
        game.make_move(1, 2, "S")  # Blue (1,2) - SCORES 1 (1,0-1,2). Blue retains turn.

        self.assertEqual(game.blue_player.score, 1)
        self.assertEqual(game.red_player.score, 0)
        self.assertEqual(game.current_turn.color, "Blue")  # Blue retains turn

    def test_general_game_winner_by_score(self):
        # Tests that the game ends only when the board is full and the high score wins.
        game = GeneralGame(3)
        # Force a score setup for simplicity
        game.blue_player.score = 2
        game.red_player.score = 1

        for r in range(3):
            for c in range(3):
                if game.board.is_cell_empty(r, c):
                    game.board.place_letter(r, c, "S")

        self.assertTrue(game.is_game_over())
        self.assertEqual(game.get_winner(), "Blue")

    def test_general_game_draw_by_score(self):
        #Tests that the game ends in a draw if scores are equal when the board is full.
        game = GeneralGame(3)
        game.blue_player.score = 1
        game.red_player.score = 1


        for r in range(3):
            for c in range(3):
                if game.board.is_cell_empty(r, c):
                    game.board.place_letter(r, c, "S")

        self.assertTrue(game.is_game_over())
        self.assertEqual(game.get_winner(), "Draw")