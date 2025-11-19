# test_controller.py
import unittest
from controller import GameController
from SimpleGame import SimpleGame
from GeneralGame import GeneralGame


class TestController(unittest.TestCase):

    def test_new_game_flow_simple(self):
        # Tests starting a new Simple game and verifying the class.
        controller = GameController()
        controller.start_new_game(3, "Simple")
        self.assertEqual(controller.game.board.size, 3)
        self.assertIsInstance(controller.game, SimpleGame)
        self.assertEqual(controller.get_current_turn(), "Blue")

    def test_new_game_flow_general(self):
        # Tests starting a new General game and verifying the class.
        controller = GameController()
        controller.start_new_game(5, "General")
        self.assertEqual(controller.game.board.size, 5)
        self.assertIsInstance(controller.game, GeneralGame)
        self.assertEqual(controller.get_current_turn(), "Blue")

    def test_encapsulation_methods(self):
        #Tests controller methods for turn/letter/status.
        controller = GameController()
        controller.start_new_game(3, "Simple")

        # Test letter getter
        self.assertEqual(controller.get_current_player_letter(), "S")
        controller.game.blue_player.set_letter("O")
        self.assertEqual(controller.get_current_player_letter(), "O")

        # Test status getter (simple game initial state)
        self.assertEqual(controller.get_game_status(), "Current Turn: Blue")


if __name__ == "__main__":
    unittest.main()