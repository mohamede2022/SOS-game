import tkinter as tk

class GUIBoard(tk.Frame):
    # Initialize the GUI board
    def __init__(self, master, controller, size=3):
        super().__init__(master)
        self.controller = controller
        self.size = size
        self.cells = []
        self.build_board()

    # Build or rebuild the board buttons
    def build_board(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.cells = []
        for r in range(self.size):
            row_buttons = []
            for c in range(self.size):
                btn = tk.Button(self, text="", width=4, height=2,
                                font=("Arial", 18),
                                command=lambda r=r, c=c: self.handle_click(r, c))
                btn.grid(row=r, column=c)
                row_buttons.append(btn)
            self.cells.append(row_buttons)

    # Handle a button click
    def handle_click(self, row, col):
        current_turn = self.controller.get_current_turn()
        player = self.controller.game.current_turn
        letter = player.letter_choice

        if self.controller.handle_move(row, col, letter):
            color = "blue" if current_turn == "Blue" else "red"
            self.cells[row][col].config(text=letter, fg=color)
            self.master.update_turn_label()
