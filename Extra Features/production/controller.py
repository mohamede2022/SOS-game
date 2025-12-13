from SimpleGame import SimpleGame
from GeneralGame import GeneralGame
from typing import List


class GameController:
    def __init__(self):
        # Default start
        self.game = SimpleGame(3, blue_type="Human", red_type="Human")
        self.is_recording = False
        self.is_replaying = False
        self.replay_moves = []
        self.replay_index = 0

    def start_new_game(self, size: int, mode: str, blue_type: str, red_type: str):
        if mode == "Simple":
            self.game = SimpleGame(size, blue_type, red_type)
        elif mode == "General":
            self.game = GeneralGame(size, blue_type, red_type)
        else:
            raise ValueError(f"Unknown game mode: {mode}")

        self.is_replaying = False
        self.replay_moves = []
        self.replay_index = 0

    def handle_move(self, row: int, col: int, letter: str) -> bool:
        return self.game.make_move(row, col, letter)

    def is_current_player_computer(self) -> bool:
        return self.game.is_current_player_computer()

    # FEATURE 1:  Computer Move
    def handle_computer_move(self) -> tuple:
        if self.game.is_game_over():
            return (-1, -1, "")

        # Got the move from the ComputerPlayer's Minimax logic
        r, c, letter = self.game.get_computer_move()

        if r != -1:
            # Apply the move to the game logic
            self.game.make_move(r, c, letter)
            return (r, c, letter)

        return (-1, -1, "")

    # Feature 2: Helpers
    def get_scored_lines(self):
        if hasattr(self.game, 'scored_lines'):
            return self.game.scored_lines
        return []

    def get_player_scores(self):
        # Access scores directly from the player objects
        return self.game.blue_player.score, self.game.red_player.score

    def get_winner_color(self):
        winner_data = self.game.get_winner()
        if winner_data == "Draw": return "Draw"
        if isinstance(winner_data, tuple): return winner_data[0]
        return winner_data

    # Record/Replay methods
    def record_game_to_file(self, filename: str):
        mode = "General" if isinstance(self.game, GeneralGame) else "Simple"
        size = self.game.board.size
        # Check for ComputerPlayer type
        b_type = "Computer" if self.game.blue_player.__class__.__name__ == "ComputerPlayer" else "Human"
        r_type = "Computer" if self.game.red_player.__class__.__name__ == "ComputerPlayer" else "Human"

        try:
            with open(filename, "w") as f:
                f.write(f"{mode},{size},{b_type},{r_type}\n")
                for move in self.game.move_history:
                    f.write(f"{move[0]},{move[1]},{move[2]}\n")
            return True
        except IOError:
            return False

    def load_game_from_file(self, filename: str) -> bool:
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return False
        if not lines: return False

        try:
            setup = lines[0].strip().split(',')
            mode, size, b_type, r_type = setup[0], int(setup[1]), setup[2], setup[3]
        except (ValueError, IndexError):
            return False

        self.start_new_game(size, mode, b_type, r_type)
        self.replay_moves = []
        for line in lines[1:]:
            parts = line.strip().split(',')
            if len(parts) == 3:
                self.replay_moves.append((int(parts[0]), int(parts[1]), parts[2]))

        self.is_replaying = True
        self.replay_index = 0
        return True

    def get_next_replay_move(self):
        if not self.is_replaying or self.replay_index >= len(self.replay_moves):
            self.is_replaying = False
            return False
        r, c, letter = self.replay_moves[self.replay_index]
        self.game.make_move(r, c, letter)
        self.replay_index += 1
        return True

    def get_current_player_letter(self) -> str:
        return self.game.current_turn.letter_choice

    def get_current_turn(self) -> str:
        return self.game.current_turn.color

    # Feature 2 Integration: Improved Status Display
    def get_game_status(self) -> str:
        blue_score, red_score = self.get_player_scores()

        if self.game.is_game_over():
            winner = self.game.get_winner()

            # Simple Game: winner is a string
            if isinstance(winner, str):
                return f"Game Over! Winner: {winner}"

            # General Game: winner is tuple displaying winner_color and score data.
            winner_color = winner[0]
            return f"Game Over! Winner: {winner_color} (Blue: {blue_score}, Red: {red_score})"

        # General Game in progress status
        if isinstance(self.game, GeneralGame):
            return f"Turn: {self.get_current_turn()} | Blue: {blue_score} - Red: {red_score}"

        # Simple Game in progress status
        return f"Current Turn: {self.get_current_turn()}"

    def get_board(self) -> List[List[str]]:
        return self.game.board.grid

    def set_player_letter(self, color: str, letter: str):
        if color == "Blue":
            self.game.blue_player.set_letter(letter)
        else:
            self.game.red_player.set_letter(letter)