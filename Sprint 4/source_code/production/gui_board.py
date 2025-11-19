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

        for r in range(self.size):
            for c in range(self.size):
                letter = self.controller.get_board()[r][c]
                if letter != "":
                    # Placed cells are disabled
                    self.cells[r][c].config(text=letter, fg="green", state=tk.DISABLED)
                else:
                    self.cells[r][c].config(state=tk.NORMAL)

        # Disable board if the starting player is a computer
        if self.controller.is_current_player_computer():
            self.disable_board()

    def handle_click(self, row, col):
        # 1. Check if game is over before processing move
        if self.controller.game.is_game_over():
            if self.board_update_callback:
                self.board_update_callback()
            return

        # 2. Prevent human move if it's the computer's turn
        if self.controller.is_current_player_computer():
            # Show the message but don't recall the update.
            messagebox.showinfo("Wait", "It is the computer's turn.")
            return

        current_turn = self.controller.get_current_turn()
        letter = self.controller.get_current_player_letter()

        if self.controller.handle_move(row, col, letter):
            color = "blue" if current_turn == "Blue" else "red"
            self.cells[row][col].config(text=letter, fg=color)
            if self.board_update_callback:
                self.board_update_callback()
        else:
            # Invalid move cell occupied
            messagebox.showerror("Error", "That cell is already occupied.")

    def disable_board(self):
        # Disables all buttons on the board.
        for r in range(self.size):
            for c in range(self.size):
                self.cells[r][c].config(state=tk.DISABLED)

    def enable_board(self):
        #Enables only empty cells on the board for the human player.
        for r in range(self.size):
            for c in range(self.size):
                if self.controller.get_board()[r][c] == "":
                    self.cells[r][c].config(state=tk.NORMAL)
                else:
                    # Keep placed letters disabled
                    self.cells[r][c].config(state=tk.DISABLED)