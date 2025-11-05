
import tkinter as tk


class GUIBoard(tk.Frame):

    def __init__(self, master, controller, size=3, board_update_callback=None):
        super().__init__(master)
        self.controller = controller
        self.size = size
        self.cells = []
        self.board_update_callback = board_update_callback
        self.build_board()

    def build_board(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.cells = []
        for r in range(self.size):
            row_buttons = []
            for c in range(self.size):
                # The lambda r=r, c=c is correct for Tkinter
                btn = tk.Button(self, text="", width=4, height=2,
                                font=("Arial", 18),
                                command=lambda r=r, c=c: self.handle_click(r, c))
                btn.grid(row=r, column=c)
                row_buttons.append(btn)
            self.cells.append(row_buttons)

        # Repopulate board with existing state
        for r in range(self.size):
            for c in range(self.size):
                letter = self.controller.get_board()[r][c]
                if letter != "":
                    self.cells[r][c].config(text=letter, fg="black")

    def handle_click(self, row, col):
        # Check if game is over before processing move
        if self.controller.game.is_game_over():
            if self.board_update_callback:
                self.board_update_callback()
            return

        current_turn = self.controller.get_current_turn()
        letter = self.controller.get_current_player_letter()

        if self.controller.handle_move(row, col, letter):
            # Update the button and the turn label using the callback
            color = "blue" if current_turn == "Blue" else "red"
            self.cells[row][col].config(text=letter, fg=color)
            if self.board_update_callback:
                self.board_update_callback()