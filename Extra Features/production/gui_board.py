import tkinter as tk
from tkinter import messagebox


class GUIBoard(tk.Canvas):
    def __init__(self, master, controller, size=3, board_update_callback=None):
        # Initialize the Canvas
        super().__init__(master, width=500, height=500, bg="#333333", highlightthickness=0)
        self.controller = controller
        self.size = size
        self.board_update_callback = board_update_callback

        # Bind the mouse click event to the Canvas logic
        self.bind("<Button-1>", self.handle_click)

        self.cell_size = 500 / self.size
        self.build_board()

    def build_board(self):
        self.delete("all")  # Clear everything and create again
        self.cell_size = 500 / self.size

        for r in range(self.size):
            for c in range(self.size):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # 1. Draw the Button background (Rectangle), I taged it with its row/col so i can find it later if needed
                self.create_rectangle(x1, y1, x2, y2,
                                      fill="lightgray", outline="black", width=2,
                                      tags=f"cell_{r}_{c}")

                # 2. Draw the Text empty at start
                self.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                 text="", font=("Arial", int(self.cell_size / 2)),
                                 fill="black",
                                 tags=f"text_{r}_{c}")

        self.update_board_display()

    def update_board_display(self):
        grid = self.controller.get_board()
        for r in range(self.size):
            for c in range(self.size):
                letter = grid[r][c]

                # Find the text item for this cell and update it
                self.itemconfigure(f"text_{r}_{c}", text=letter)


        # Redraw the lines on top of the letters for SOS
        self.draw_scored_lines()

    def draw_scored_lines(self):
        # Remove old lines to prevent duplicates
        self.delete("sos_line")

        scored_lines = self.controller.get_scored_lines()
        if not scored_lines: return

        for (r1, c1), (r2, c2), color in scored_lines:
            # Calculate center points of the start and end cells of scored SOS's
            x1 = c1 * self.cell_size + self.cell_size / 2
            y1 = r1 * self.cell_size + self.cell_size / 2
            x2 = c2 * self.cell_size + self.cell_size / 2
            y2 = r2 * self.cell_size + self.cell_size / 2

            # Line color
            line_color = "RoyalBlue" if color == "Blue" else "Red"

            # Draw the line
            self.create_line(x1, y1, x2, y2, width=8, fill=line_color,
                             tags="sos_line", capstyle="round")
        self.tag_raise("sos_line")

    def handle_click(self, event):
        # Ignore clicks if game over, replay or computer turn
        if self.controller.game.is_game_over() or self.controller.is_replaying:
            return
        if self.controller.is_current_player_computer():
            return

        # which Row or Column was clicked based on Mouse
        col = int(event.x // self.cell_size)
        row = int(event.y // self.cell_size)

        # Ensure click is inside the board
        if 0 <= row < self.size and 0 <= col < self.size:
            letter = self.controller.get_current_player_letter()

            if self.controller.handle_move(row, col, letter):
                if self.board_update_callback:
                    self.board_update_callback()
            else:
                messagebox.showerror("Error", "Cell occupied.")

    def disable_board(self):
        # For Stopping interaction with board
        pass

    def enable_board(self):
        pass