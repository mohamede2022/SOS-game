import unittest
from player import ComputerPlayer
from board import Board
from SOSGame import SOSGame
from SimpleGame import SimpleGame


class TestComputerPlayer(unittest.TestCase):
    def setUp(self):
        self.board = Board(3)
        self.computer_blue = ComputerPlayer("Blue")
        self.computer_red = ComputerPlayer("Red")

    def test_instantiation(self):
        # Tests that a ComputerPlayer object is instantiated correctly.
        self.assertEqual(self.computer_blue.color, "Blue")
        self.assertEqual(self.computer_blue.letter_choice, "S")
        self.assertEqual(self.computer_red.score, 0)
        self.computer_red.set_letter("O")
        self.assertEqual(self.computer_red.letter_choice, "O")

    def test_non_sos_move(self):
        # Tests that the computer makes a valid move when no immediate SOS is possible.
        self.board.place_letter(0, 0, "S")
        self.board.place_letter(0, 1, "O")
        r, c, letter = self.computer_blue.get_move(self.board, "Simple")

        # Check that the move is within bounds and the cell is empty
        self.assertTrue(0 <= r < 3)
        self.assertTrue(0 <= c < 3)
        self.assertTrue(self.board.is_cell_empty(r, c))
        self.assertEqual(letter, "S")

    def test_winning_move_horizontal(self):
        #Tests that the computer prioritizes a horizontal SOS move.
        self.board.place_letter(1, 0, "S")
        self.board.place_letter(1, 2, "S")

        # Computer's choice is 'S', but it should look for an 'O' winning move.
        r, c, letter = self.computer_blue.get_move(self.board, "Simple")

        self.assertEqual(r, 1)
        self.assertEqual(c, 1)
        self.assertEqual(letter, "O")

    def test_winning_move_vertical(self):
        # Tests that the computer prioritizes a vertical SOS move.
        self.board.place_letter(0, 1, "S")
        self.board.place_letter(2, 1, "S")
        r, c, letter = self.computer_red.get_move(self.board, "Simple")

        self.assertEqual(r, 1)
        self.assertEqual(c, 1)
        self.assertEqual(letter, "O")

    def test_winning_move_diagonal_start_S(self):
        # Tests that the computer prioritizes a diagonal SOS move.
        self.board.place_letter(0, 0, "S")
        self.board.place_letter(1, 1, "O")
        r, c, letter = self.computer_blue.get_move(self.board, "Simple")

        self.assertEqual(r, 2)
        self.assertEqual(c, 2)
        self.assertEqual(letter, "S")

    def test_game_integration_simple_win(self):
        # Tests that the SimpleGame correctly executes a computer player's move and ends the game.
        game = SimpleGame(3, blue_type="Computer", red_type="Human")
        game.blue_player.set_letter("S")
        game.board.place_letter(0, 0, "S")
        game.board.place_letter(0, 1, "O")
        game.current_turn = game.blue_player

        # Get the move calculated by the computer
        r, c, letter = game.get_computer_move()

        self.assertEqual(r, 0)
        self.assertEqual(c, 2)
        self.assertEqual(letter, "S")

        # Execute the move and check game state
        game.make_move(r, c, letter)
        self.assertTrue(game.is_game_over())
        self.assertEqual(game.get_winner(), "Blue")
        self.assertEqual(game.blue_player.score, 1)
        self.assertEqual(game.board.grid[0][2], "S")