from abc import ABC, abstractmethod
import random
from typing import TYPE_CHECKING

# To prevent circular import at runtime
if TYPE_CHECKING:
    from board import Board


class Player(ABC):
    #Abstract base class for all player types.

    def __init__(self, color):
        self.color = color
        self.letter_choice = "S"
        self.score = 0

    def set_letter(self, letter):
        self.letter_choice = letter

    @abstractmethod
    def get_move(self, board: 'Board', game_mode: str) -> tuple:
        # Abstract method for getting a move (row, col, letter).
        pass


class HumanPlayer(Player):
    # Represents a human player whose moves come from the GUI.

    def __init__(self, color):
        super().__init__(color)

    def get_move(self, board, game_mode) -> tuple:
        # Human player move is handled by the GUI click.
        raise NotImplementedError("Human moves are handled by the GUI.")


class ComputerPlayer(Player):
    # Represents a computer player with move making logic.

    def __init__(self, color):
        super().__init__(color)

    def get_move(self, board: 'Board', game_mode: str) -> tuple:
        # Calculates a move: prioritize SOS, otherwise make a random move.
        size = board.size
        empty_cells = []
        for r in range(size):
            for c in range(size):
                if board.is_cell_empty(r, c):
                    empty_cells.append((r, c))

        # Check for a winning move SOS
        for r, c in empty_cells:
            for letter in ["S", "O"]:
                # Temporarily place the letter to check
                board.grid[r][c] = letter
                if self._check_for_sos_at(board, r, c):
                    # Found a move that scores
                    board.grid[r][c] = ""  # Undo the temporary placement
                    return (r, c, letter)
                board.grid[r][c] = ""

        # If no winning move, choose a random cell and the player's current letter choice
        if empty_cells:
            r, c = random.choice(empty_cells)
            letter = self.letter_choice
            return (r, c, letter)
        return (-1, -1, "")

    def _check_for_sos_at(self, board: 'Board', r, c):
        # Checks if a move at (r, c) with the letter currently placed forms an SOS.
        grid = board.grid
        size = board.size
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            # Check 1: SOS
            if grid[r][c] == "S":
                r2, c2 = r + dr, c + dc
                r3, c3 = r + 2 * dr, c + 2 * dc
                if (0 <= r3 < size and 0 <= c3 < size and
                        grid[r2][c2] == "O" and grid[r3][c3] == "S"):
                    return True

            # Check 2: SOS
            if grid[r][c] == "O":
                r_prev, c_prev = r - dr, c - dc
                r_next, c_next = r + dr, c + dc
                if (0 <= r_prev < size and 0 <= c_prev < size and
                        0 <= r_next < size and 0 <= c_next < size):
                    if grid[r_prev][c_prev] == "S" and grid[r_next][c_next] == "S":
                        return True

            # Check 3: SOS
            if grid[r][c] == "S":
                r_prev, c_prev = r - dr, c - dc
                r_prev_2, c_prev_2 = r - 2 * dr, c - 2 * dc
                if (0 <= r_prev_2 < size and 0 <= c_prev_2 < size):
                    if grid[r_prev_2][c_prev_2] == "S" and grid[r_prev][c_prev] == "O":
                        return True

        return False