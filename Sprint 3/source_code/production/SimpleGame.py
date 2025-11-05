# Subclass
from SOSGame import SOSGame #Inheriting from the Base Class (SOSGame)

class SimpleGame(SOSGame):
    def __init__(self, size=3):
        super().__init__(size)
        self._is_over = False
        self._winner: str = "Game in progress"

    def is_game_over(self):
        return self._is_over

    def get_winner(self):
        # If blue scored, and red didn't, blue is the winner.
        if self.blue_player.score > 0 and self.red_player.score == 0:
            return self.blue_player.color
        # If red scored, and blue didn't, red is the winner.
        if self.red_player.score > 0 and self.blue_player.score == 0:
            return self.red_player.color
        return "Draw" # Only reached if game over and no score

    def check_game_end(self, sos_found):
        # Ends the game if an SOS is found or the board is full.
        if sos_found > 0:
            # Immediately set the winner to the current player
            self._winner = self.current_turn.color
            self._is_over = True
        elif self.board.is_full():
            self._is_over = True
            # Only check for draw/winner if the board fills up without an earlier SOS
            if self.blue_player.score == 0 and self.red_player.score == 0:
                self._winner = "Draw"
            elif self.blue_player.score > self.red_player.score:
                self._winner = self.blue_player.color
            elif self.red_player.score > self.blue_player.score:
                self._winner = self.red_player.color