
from SimpleGame import SimpleGame
from GeneralGame import GeneralGame
from typing import List


class GameController:
    #Manages the interaction between the GUI and the Game logic.

    def __init__(self):
        self.game = SimpleGame(3)

    def start_new_game(self, size: int, mode: str):
        # Initializes a new game based on the selected mode and size.
        if mode == "Simple":
            self.game = SimpleGame(size)
        elif mode == "General":
            self.game = GeneralGame(size)
        else:
            raise ValueError(f"Unknown game mode: {mode}")

    def handle_move(self, row: int, col: int, letter: str) -> bool:
        # Processes a move request and updates the game.
        return self.game.make_move(row, col, letter)

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
        """Sets the letter choice for the specified player, hiding the Model's internal structure."""
        if color == "Blue":
            self.game.blue_player.set_letter(letter)
        elif color == "Red":
            self.game.red_player.set_letter(letter)