from board import Board
from player import Player

class Game:
    # Initialize a new game
    def __init__(self):
        self.board = Board(3)
        self.mode = "Simple"
        self.blue_player = Player("Blue")
        self.red_player = Player("Red")
        self.current_turn = self.blue_player

    def new_game(self, size, mode):
        self.mode = mode
        self.board.reset(size)
        self.current_turn = self.blue_player

    def make_move(self, row, col, letter):
        if self.board.place_letter(row, col, letter):
            self.toggle_turn()
            return True
        return False

    # Switch turns between players
    def toggle_turn(self):
        if self.current_turn == self.blue_player:
            self.current_turn = self.red_player
        else:
            self.current_turn = self.blue_player
