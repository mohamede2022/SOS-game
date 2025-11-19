class Board:
    # Initialize the board size
    def __init__(self, size=3):
        self.size = size
        self.grid = [["" for _ in range(size)] for _ in range(size)]

    def reset(self, size):
        self.size = size
        self.grid = [["" for _ in range(size)] for _ in range(size)]

    def is_cell_empty(self, row, col):
        return self.grid[row][col] == ""

    def place_letter(self, row, col, letter):
        if self.is_cell_empty(row, col):
            self.grid[row][col] = letter
            return True
        return False

    # Check if the board is full
    def is_full(self):
        return all(cell != "" for row in self.grid for cell in row)
