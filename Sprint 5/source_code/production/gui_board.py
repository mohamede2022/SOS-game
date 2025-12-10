# gui_board.py
import tkinter as tk
from tkinter import messagebox


class GUIBoard(tk.Frame):
    def __init__(self, master, controller, size=3, board_update_callback=None):
        super().__init__(master)
        self.controller = controller
        self.size = size
        self.cells = []
        self.board_update_callback = board_update_callback
        self.build_board()

    def build_board(self):
        for widget in self.winfo_children(): widget.destroy()
        self.cells = []
        for r in range(self.size):
            row_buttons = []
            for c in range(self.size):
                btn = tk.Button(self, text="", width=4, height=2, font=("Arial", 18),
                                command=lambda r=r, c=c: self.handle_click(r, c))
                btn.grid(row=r, column=c)
                row_buttons.append(btn)
            self.cells.append(row_buttons)
        self.update_board_display()

    # Refresh board from controller state (for replay)
    def update_board_display(self):
        grid = self.controller.get_board()
        for r in range(self.size):
            for c in range(self.size):
                letter = grid[r][c]
                if letter != "":
                    self.cells[r][c].config(text=letter, state=tk.DISABLED, disabledforeground="black")
                else:
                    self.cells[r][c].config(text="", state=tk.NORMAL)

        if self.controller.is_current_player_computer() and not self.controller.is_replaying:
            self.disable_board()  # Prevent clicks during computer turn

    def handle_click(self, row, col):
        # Prevent clicks during replay or game over
        if self.controller.game.is_game_over() or self.controller.is_replaying:
            return

        if self.controller.is_current_player_computer():
            return

        current_turn = self.controller.get_current_turn()
        letter = self.controller.get_current_player_letter()

        if self.controller.handle_move(row, col, letter):
            color = "blue" if current_turn == "Blue" else "red"
            self.cells[row][col].config(text=letter, disabledforeground=color)
            if self.board_update_callback:
                self.board_update_callback()
        else:
            messagebox.showerror("Error", "Cell occupied.")

    def disable_board(self):
        for r in range(self.size):
            for c in range(self.size):
                self.cells[r][c].config(state=tk.DISABLED)

    def enable_board(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.controller.get_board()[r][c] == "":
                    self.cells[r][c].config(state=tk.NORMAL)