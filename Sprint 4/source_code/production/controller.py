from SimpleGame import SimpleGame
from GeneralGame import GeneralGame
from typing import List


class GameController:
    # Manages the interaction between the GUI and the Game logic.

    def __init__(self):
        # Default initialization includes player types for Sprint 4
        self.game = SimpleGame(3, blue_type="Human", red_type="Human")

    def start_new_game(self, size: int, mode: str, blue_type: str, red_type: str):
        # Initializes a new game based on the selected mode, size, and player types.
        if mode == "Simple":
            self.game = SimpleGame(size, blue_type, red_type)
        elif mode == "General":
            self.game = GeneralGame(size, blue_type, red_type)
        else:
            raise ValueError(f"Unknown game mode: {mode}")

    def handle_move(self, row: int, col: int, letter: str) -> bool:
        # Processes a human move request and updates the game.
        return self.game.make_move(row, col, letter)

    # Methods for Computer Player Management

    def is_current_player_computer(self) -> bool:
        # Returns True if the current player is a computer.
        return self.game.is_current_player_computer()

    def handle_computer_move(self) -> tuple:
        # Requests the computer's move from the game model and executes it. Returns: (r, c, letter) of the move made.
        if self.game.is_game_over():
            return (-1, -1, "")

        r, c, letter = self.game.get_computer_move()

        # Check for invalid move
        if r != -1:
            # Execute the move found by the computer's logic
            self.game.make_move(r, c, letter)
            return (r, c, letter)
        return (-1, -1, "")

    def get_current_player_letter(self) -> str:
        # Returns the current player's selected letter (S or O).
        return self.game.current_turn.letter_choice

    def get_current_turn(self) -> str:
        # Returns the color of the player whose turn it is.
        return self.game.current_turn.color

    def get_game_status(self) -> str:
        # Returns the current turn or the game over message with the winner/score.
        if self.game.is_game_over():
            winner = self.game.get_winner()
            if winner == "Draw":
                return "Game Over! Result: Draw"
            if isinstance(self.game, GeneralGame):
                return f"Game Over! Winner: {winner} (Blue: {self.game.blue_player.score}, Red: {self.game.red_player.score})"
            return f"Game Over! Winner: {winner}"

        if isinstance(self.game, GeneralGame):
            return f"Current Turn: {self.get_current_turn()} (Blue Score: {self.game.blue_player.score}, Red Score: {self.game.red_player.score})"

        return f"Current Turn: {self.get_current_turn()}"

    def get_board(self) -> List[List[str]]:
        # Returns the current board grid.
        return self.game.board.grid

    def set_player_letter(self, color: str, letter: str):
        # Sets the letter choice for the specified player.
        if color == "Blue":
            self.game.blue_player.set_letter(letter)
        else:
            self.game.red_player.set_letter(letter)