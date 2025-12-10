import unittest
from game import Game

class TestGame(unittest.TestCase):
    # Test that new_game resets the board
    def test_new_game_resets_board(self):
        game = Game()
        game.board.place_letter(0, 0, "S")
        game.new_game(4, "General")
        self.assertEqual(game.board.size, 4)
        self.assertTrue(all(cell == "" for row in game.board.grid for cell in row))

    # Test that turns toggle correctly
    def test_turn_toggle(self):
        game = Game()
        first_turn = game.current_turn
        game.make_move(0, 0, "S")
        self.assertNotEqual(game.current_turn, first_turn)

if __name__ == "__main__":
    unittest.main()
