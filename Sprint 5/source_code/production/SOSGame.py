# SOSGame.py
from board import Board
from player import HumanPlayer, ComputerPlayer
from abc import ABC, abstractmethod


class SOSGame(ABC):
    def __init__(self, size=3, blue_type="Human", red_type="Human"):
        self.board = Board(size)
        self.blue_player = self._create_player("Blue", blue_type)
        self.red_player = self._create_player("Red", red_type)
        self.current_turn = self.blue_player
        self.blue_player.score = 0
        self.red_player.score = 0
        # Store move history for recording
        self.move_history = []

    def _create_player(self, color, player_type):
        if player_type == "Human":
            return HumanPlayer(color)
        elif player_type == "Computer":
            return ComputerPlayer(color)
        else:
            raise ValueError(f"Unknown player type: {player_type}")

    def new_game(self, size, blue_type, red_type):
        self.board.reset(size)
        self.blue_player = self._create_player("Blue", blue_type)
        self.red_player = self._create_player("Red", red_type)
        self.current_turn = self.blue_player
        self.blue_player.score = 0
        self.red_player.score = 0
        self.move_history = []

    def is_current_player_computer(self) -> bool:
        return isinstance(self.current_turn, ComputerPlayer)

    def get_computer_move(self) -> tuple:
        if self.is_current_player_computer():
            game_mode = self.__class__.__name__.replace("Game", "")
            return self.current_turn.get_move(self.board, game_mode)
        return (-1, -1, "")

    def check_for_sos(self, r, c):
        sos_found = 0
        grid = self.board.grid
        size = self.board.size
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            # Check 1
            r3, c3 = r + 2 * dr, c + 2 * dc
            if 0 <= r3 < size and 0 <= c3 < size:
                if grid[r][c] == "S" and grid[r + dr][c + dc] == "O" and grid[r3][c3] == "S":
                    self.current_turn.score += 1
                    sos_found += 1
            # Check 2
            r_prev, c_prev = r - dr, c - dc
            r_next, c_next = r + dr, c + dc
            if (0 <= r_prev < size and 0 <= c_prev < size and
                    0 <= r_next < size and 0 <= c_next < size):
                if grid[r][c] == "O" and grid[r_prev][c_prev] == "S" and grid[r_next][c_next] == "S":
                    self.current_turn.score += 1
                    sos_found += 1
            # Check 3
            r_prev_2, c_prev_2 = r - 2 * dr, c - 2 * dc
            if 0 <= r_prev_2 < size and 0 <= c_prev_2 < size:
                if grid[r][c] == "S" and grid[r_prev_2][c_prev_2] == "S" and grid[r_prev][c_prev] == "O":
                    self.current_turn.score += 1
                    sos_found += 1
        return sos_found

    def make_move(self, row, col, letter):
        if self.board.place_letter(row, col, letter):
            # NEW: Record the move
            self.move_history.append((row, col, letter))

            sos_found = self.check_for_sos(row, col)
            self.check_game_end(sos_found)
            if not self.is_game_over():
                if sos_found == 0:
                    self.toggle_turn()
            return True
        return False

    def toggle_turn(self):
        if self.current_turn == self.blue_player:
            self.current_turn = self.red_player
        else:
            self.current_turn = self.blue_player

    @abstractmethod
    def is_game_over(self):
        pass

    @abstractmethod
    def get_winner(self):
        pass

    @abstractmethod
    def check_game_end(self, sos_found):
        pass