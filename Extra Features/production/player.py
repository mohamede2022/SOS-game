from abc import ABC, abstractmethod
import random
import math
from typing import TYPE_CHECKING
import copy
from board import Board


class Player(ABC):
    # Abstract base class for all player types.

    def __init__(self, color, max_depth=0):
        self.color = color
        self.letter_choice = "S"
        self.score = 0
        self.max_depth = max_depth  # Difficulty level

    def set_letter(self, letter):
        self.letter_choice = letter

    @abstractmethod
    def get_move(self, board: 'Board', game_mode: str) -> tuple:
        pass


class HumanPlayer(Player):
    def __init__(self, color, max_depth=0):
        super().__init__(color, max_depth)

    def get_move(self, board, game_mode) -> tuple:
        raise NotImplementedError("Human moves are handled by the GUI.")


class ComputerPlayer(Player):
    def __init__(self, color, max_depth=4):  # Increased default depth for better AI
        super().__init__(color, max_depth)
        self.opponent_color = "Red" if color == "Blue" else "Blue"

    def get_move(self, board: 'Board', game_mode: str) -> tuple:
        # Feature 1: MINIMAX Algorithm

        valid_moves = []
        size = board.size
        for r in range(size):
            for c in range(size):
                if board.is_cell_empty(r, c):
                    valid_moves.append((r, c))

        if not valid_moves:
            return -1, -1,

        best_score = -math.inf
        best_move = None

        # Shuffle to ensure random choice among equal best moves
        random.shuffle(valid_moves)

        # deep copy of the grid to simulate moves without changing the real board
        grid_copy = [row[:] for row in board.grid]


        for r, c in valid_moves:
            # The AI evaluates game playing 'S' and 'O'
            for letter in ['S', 'O']:

                grid_copy[r][c] = letter

                points_scored = self._count_sos_at(grid_copy, size, r, c)

                # Determine if the current player (the computer) keeps the turn
                is_turn_kept = (points_scored > 0) and (game_mode == "General")

                # The minimax function now tracks the score difference from the computer's perspective.
                score = self.minimax(
                    grid_copy,
                    size,
                    self.max_depth - 1,
                    -math.inf,
                    math.inf,
                    is_turn_kept,
                    points_scored
                )

                grid_copy[r][c] = ""

                if score > best_score:
                    best_score = score
                    best_move = (r, c, letter)

        if best_move:
            # Set the computer's letter choice to the determined best letter
            self.letter_choice = best_move[2]
            return best_move


        r, c = random.choice(valid_moves)
        return r, c, self.letter_choice

    def minimax(self, grid, size, depth, alpha, beta, is_maximizing, score_diff):
        # Base Case: Max depth reached or board full

        # Identify empty cells for board full check
        empty_cells = []
        for r in range(size):
            for c in range(size):
                if grid[r][c] == "":
                    empty_cells.append((r, c))

        if depth == 0 or not empty_cells:
            # Return the score difference at the end of the simulation
            return score_diff

        if is_maximizing:
            max_eval = -math.inf
            for r, c in empty_cells:
                for letter in ['S', 'O']:
                    grid[r][c] = letter
                    points = self._count_sos_at(grid, size, r, c)

                    # General game rule: If score, current player goes again still maximizing
                    next_is_maximizing = (points > 0)

                    # New score difference is increased by the points the current player (Computer) scored
                    new_score_diff = score_diff + points

                    eval_score = self.minimax(
                        grid, size, depth - 1, alpha, beta,
                        next_is_maximizing,
                        new_score_diff
                    )

                    grid[r][c] = ""
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha: break
                if beta <= alpha: break
            return max_eval
        else:  # Minimizing Player (The Human Opponent)
            min_eval = math.inf
            for r, c in empty_cells:
                for letter in ['S', 'O']:
                    grid[r][c] = letter
                    points = self._count_sos_at(grid, size, r, c)

                    # General game rule: If opponent score they go again still minimizing
                    next_is_maximizing = not (points > 0)

                    # New score difference is decreased by the points the opponent scored
                    new_score_diff = score_diff - points

                    eval_score = self.minimax(
                        grid, size, depth - 1, alpha, beta,
                        next_is_maximizing,
                        new_score_diff
                    )

                    grid[r][c] = ""
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha: break
                if beta <= alpha: break
            return min_eval

    def _count_sos_at(self, grid, size, r, c):
        # Helper to count how many SOSs are formed by a move at (r,c)
        count = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            # Check 1
            if grid[r][c] == "S":
                if (0 <= r + 2 * dr < size and 0 <= c + 2 * dc < size and
                        grid[r + dr][c + dc] == "O" and grid[r + 2 * dr][c + 2 * dc] == "S"):
                    count += 1
            # Check 2
            if grid[r][c] == "O":
                if (0 <= r - dr < size and 0 <= c - dc < size and
                        0 <= r + dr < size and 0 <= c + dc < size and
                        grid[r - dr][c - dc] == "S" and grid[r + dr][c + dc] == "S"):
                    count += 1
            # Check 3
            if grid[r][c] == "S":
                if (0 <= r - 2 * dr < size and 0 <= c - 2 * dc < size and
                        grid[r - dr][c - dc] == "O" and grid[r - 2 * dr][c - 2 * dc] == "S"):
                    count += 1
        return count