# Subclass
from SOSGame import SOSGame #Inheriting from the Base Class (SOSGame)


class GeneralGame(SOSGame):
    def __init__(self, size=3, blue_type="Human", red_type="Human"):
        # Pass player types to the base class constructor
        super().__init__(size, blue_type, red_type)

    def is_game_over(self):
        # General game ends only when the board is full
        return self.board.is_full()

    def get_winner(self):
        if not self.is_game_over():
            return "Game in progress"

        blue_score = self.blue_player.score
        red_score = self.red_player.score

        if blue_score > red_score:
            return self.blue_player.color
        elif red_score > blue_score:
            return self.red_player.color
        else:
            return "Draw"

    def check_game_end(self, sos_found):
        # Scoring is handled in the base class so no change to game end state here.
        pass