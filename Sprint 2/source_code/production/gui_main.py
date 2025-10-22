import tkinter as tk
from tkinter import ttk
from controller import GameController
from gui_board import GUIBoard

class SOSApp(tk.Tk):
    # Initialize the main app
    def __init__(self):
        super().__init__()
        self.title("SOS Game")
        self.geometry("600x600")

        self.controller = GameController()
        self.board_frame = None

        self.mode_var = tk.StringVar(value="Simple")
        self.size_var = tk.StringVar(value="3")
        self.blue_letter = tk.StringVar(value="S")
        self.red_letter = tk.StringVar(value="S")

        self.create_widgets()

    # Create UI elements
    def create_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10)

        # Mode selection
        tk.Label(top_frame, text="Game Mode:").grid(row=0, column=0)
        tk.Radiobutton(top_frame, text="Simple", variable=self.mode_var, value="Simple").grid(row=0, column=1)
        tk.Radiobutton(top_frame, text="General", variable=self.mode_var, value="General").grid(row=0, column=2)

        # Board size
        tk.Label(top_frame, text="Board Size:").grid(row=0, column=3)
        tk.Entry(top_frame, textvariable=self.size_var, width=5).grid(row=0, column=4)

        # New Game button
        tk.Button(top_frame, text="New Game", command=self.start_new_game).grid(row=0, column=5, padx=10)

        # Player sections
        player_frame = tk.Frame(self)
        player_frame.pack(pady=10)

        # Blue player
        blue_frame = tk.LabelFrame(player_frame, text="Blue Player", padx=10, pady=5)
        blue_frame.grid(row=0, column=0, padx=20)
        tk.Radiobutton(blue_frame, text="S", variable=self.blue_letter, value="S",
                       command=lambda: self.set_letter("Blue", "S")).pack(anchor="w")
        tk.Radiobutton(blue_frame, text="O", variable=self.blue_letter, value="O",
                       command=lambda: self.set_letter("Blue", "O")).pack(anchor="w")

        # Red player
        red_frame = tk.LabelFrame(player_frame, text="Red Player", padx=10, pady=5)
        red_frame.grid(row=0, column=1, padx=20)
        tk.Radiobutton(red_frame, text="S", variable=self.red_letter, value="S",
                       command=lambda: self.set_letter("Red", "S")).pack(anchor="w")
        tk.Radiobutton(red_frame, text="O", variable=self.red_letter, value="O",
                       command=lambda: self.set_letter("Red", "O")).pack(anchor="w")

        # Current Turn label
        self.turn_label = tk.Label(self, text="Current Turn: Blue", font=("Arial", 14))
        self.turn_label.pack(pady=10)

        # Game board
        self.board_frame = GUIBoard(self, self.controller, 3)
        self.board_frame.pack()

    def start_new_game(self):
        try:
            size = int(self.size_var.get())
            if size < 3:
                raise ValueError
        except ValueError:
            self.turn_label.config(text="Invalid board size. Must be ≥ 3.")
            return

        mode = self.mode_var.get()
        self.controller.start_new_game(size, mode)
        self.board_frame.size = size
        self.board_frame.build_board()
        self.update_turn_label()

    def set_letter(self, color, letter):
        if color == "Blue":
            self.controller.game.blue_player.set_letter(letter)
        else:
            self.controller.game.red_player.set_letter(letter)

    def update_turn_label(self):
        current = self.controller.get_current_turn()
        self.turn_label.config(text=f"Current Turn: {current}")

if __name__ == "__main__":
    app = SOSApp()
    app.mainloop()
