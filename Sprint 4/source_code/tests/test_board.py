import unittest
from board import Board

class TestBoard(unittest.TestCase):
    # Test board creation
    def test_board_initialization(self):
        board = Board(5)
        self.assertEqual(len(board.grid), 5)
        self.assertTrue(all(cell == "" for row in board.grid for cell in row))

    # Test placing a letter
    def test_place_letter(self):
        board = Board(3)
        placed = board.place_letter(1, 1, "S")
        self.assertTrue(placed)
        self.assertEqual(board.grid[1][1], "S")

    # Test invalid move (cell occupied)
    def test_invalid_move(self):
        board = Board(3)
        board.place_letter(0, 0, "S")
        placed = board.place_letter(0, 0, "O")
        self.assertFalse(placed)

if __name__ == "__main__":
    unittest.main()
