from game import Game

class GameController:
    def __init__(self):
        self.game = Game()

    def start_new_game(self, size, mode):
        self.game.new_game(size, mode)

    # Handle a move request
    def handle_move(self, row, col, letter):
        return self.game.make_move(row, col, letter)

    # Get current player's turn
    def get_current_turn(self):
        return self.game.current_turn.color

    # Get the current board state
    def get_board(self):
        return self.game.board.grid
