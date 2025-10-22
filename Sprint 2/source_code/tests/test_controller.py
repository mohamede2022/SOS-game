import unittest
from controller import GameController

class TestController(unittest.TestCase):
    def test_set_board_size(self):
        controller = GameController()
        controller.set_board_size(4)
        self.assertEqual(controller.board_size, 4)

    # Test starting a new game
    def test_new_game_flow(self):
        controller = GameController()
        controller.start_new_game(3, "Simple")
        self.assertEqual(controller.game.board.size, 3)
        self.assertEqual(controller.game.mode, "Simple")

if __name__ == "__main__":
    unittest.main()
