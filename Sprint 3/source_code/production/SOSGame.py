#(Base Class)
from board import Board
from player import Player
from abc import ABC, abstractmethod


class SOSGame(ABC):
    def __init__(self, size=3):
        self.board = Board(size)
        self.blue_player = Player("Blue")
        self.red_player = Player("Red")
        self.current_turn = self.blue_player
        self.blue_player.score = 0
        self.red_player.score = 0

    def new_game(self, size):
        self.board.reset(size)
        self.current_turn = self.blue_player
        self.blue_player.score = 0
        self.red_player.score = 0

    # Check for SOS in all directions
    def check_for_sos(self, r, c):
        sos_found = 0
        grid = self.board.grid
        size = self.board.size
        directions = [
            (0, 1),  # Horizontal
            (1, 0),  # Vertical
            (1, 1),  # Diagonal
            (1, -1)  # Diagonal
        ]
        for dr, dc in directions:
            # Check 1
            r3, c3 = r + 2 * dr, c + 2 * dc
            if 0 <= r3 < size and 0 <= c3 < size:
                # SOS Forward (Current is START S)
                if grid[r][c] == "S" and grid[r + dr][c + dc] == "O" and grid[r3][c3] == "S":
                    self.current_turn.score += 1
                    sos_found += 1

            # Check 2
            r_prev, c_prev = r - dr, c - dc
            r_next, c_next = r + dr, c + dc
            if (0 <= r_prev < size and 0 <= c_prev < size and
                0 <= r_next < size and 0 <= c_next < size):
                # SOS Centered (Current center letter is O )
                if grid[r][c] == "O" and grid[r_prev][c_prev] == "S" and grid[r_next][c_next] == "S":
                    self.current_turn.score += 1
                    sos_found += 1

            # Check 3
            r_prev_2, c_prev_2 = r - 2 * dr, c - 2 * dc
            r_prev, c_prev = r - dr, c - dc
            if 0 <= r_prev_2 < size and 0 <= c_prev_2 < size:
                # SOS Backward (Current ending in 'S')
                if grid[r][c] == "S" and grid[r_prev_2][c_prev_2] == "S" and grid[r_prev][c_prev] == "O":
                    self.current_turn.score += 1
                    sos_found += 1

        return sos_found

    def make_move(self, row, col, letter):
        if self.board.place_letter(row, col, letter):
            sos_found = self.check_for_sos(row, col)
            self.check_game_end(sos_found)
            if not self.is_game_over():
                if sos_found == 0:
                    self.toggle_turn()
            return True
        return False

    def toggle_turn(self):
        self.current_turn = self.red_player if self.current_turn == self.blue_player else self.blue_player

    @abstractmethod
    def check_game_end(self, sos_found):
        pass

    @abstractmethod
    def is_game_over(self):
        pass

    @abstractmethod
    def get_winner(self):
        pass