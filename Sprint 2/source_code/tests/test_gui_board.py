import unittest
from gui_board import GUIBoard

class TestGuiBoard(unittest.TestCase):
    # Test that button grid is created correctly
    def test_button_grid_creation(self):
        gui = GUIBoard(3)
        self.assertEqual(len(gui.buttons), 9)

if __name__ == "__main__":
    unittest.main()
