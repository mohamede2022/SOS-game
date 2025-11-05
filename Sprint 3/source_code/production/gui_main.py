# gui_main.py (Updated)
import tkinter as tk

from controller import GameController
from gui_board import GUIBoard


class SOSApp(tk.Tk):
    # Initialize the main app
    def __init__(self):
        super().__init__()
        self.title("SOS Game")
        self.geometry("650x650")

        self.controller = GameController()
        self.board_frame = None
        self.turn_label = None
        self.mode_var = tk.StringVar(value="Simple")
        self.size_var = tk.StringVar(value="3")
        self.blue_letter = tk.StringVar(value="S")
        self.red_letter = tk.StringVar(value="S")

        self.create_widgets()

    def create_widgets(self):
        # Control Frame (Mode, Size, New Game)
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10)

        # Mode selection
        tk.Label(top_frame, text="Game Mode:").grid(row=0, column=0, padx=5)
        tk.Radiobutton(top_frame, text="Simple", variable=self.mode_var, value="Simple").grid(row=0, column=1)
        tk.Radiobutton(top_frame, text="General", variable=self.mode_var, value="General").grid(row=0, column=2)

        # Board size
        tk.Label(top_frame, text="Board Size:").grid(row=0, column=3, padx=(15, 5))
        tk.Entry(top_frame, textvariable=self.size_var, width=5).grid(row=0, column=4)


        tk.Button(top_frame, text="New Game", command=self.start_new_game).grid(row=0, column=5, padx=15)

        # Main Game Frame (Player Options + Board + Status) ---
        main_game_frame = tk.Frame(self)
        main_game_frame.pack(pady=10, padx=10)

        # LEFT: Blue Player Options
        blue_frame = tk.LabelFrame(main_game_frame, text="Blue Player", padx=10, pady=10)
        blue_frame.grid(row=0, column=0, padx=20, pady=10, sticky="n")

        # Blue Player Letter Selection
        tk.Radiobutton(blue_frame, text="S", variable=self.blue_letter, value="S",
                       command=lambda: self.set_letter("Blue", "S")).pack(anchor="w")
        tk.Radiobutton(blue_frame, text="O", variable=self.blue_letter, value="O",
                       command=lambda: self.set_letter("Blue", "O")).pack(anchor="w")

        # CENTER: Board and Status
        center_frame = tk.Frame(main_game_frame)
        center_frame.grid(row=0, column=1, padx=10)

        # Current Turn label (Placed above the board)
        self.turn_label = tk.Label(center_frame, text="Current Turn: Blue", font=("Arial", 14))
        self.turn_label.pack(pady=10)

        # Game board
        self.board_frame = GUIBoard(center_frame, self.controller, 3, self.update_turn_label)
        self.board_frame.pack()  # The board itself uses pack/grid within its own frame

        # RIGHT: Red Player Options ---
        red_frame = tk.LabelFrame(main_game_frame, text="Red Player", padx=10, pady=10)
        red_frame.grid(row=0, column=2, padx=20, pady=10, sticky="n")

        # Red Player Letter Selection
        tk.Radiobutton(red_frame, text="S", variable=self.red_letter, value="S",
                       command=lambda: self.set_letter("Red", "S")).pack(anchor="w")
        tk.Radiobutton(red_frame, text="O", variable=self.red_letter, value="O",
                       command=lambda: self.set_letter("Red", "O")).pack(anchor="w")

    def start_new_game(self):
        try:
            size = int(self.size_var.get())
            if size < 3 or size > 10:
                raise ValueError
        except ValueError:
            self.turn_label.config(text="Invalid board size. Must be an integer between 3 and 10.")
            return

        mode = self.mode_var.get()
        self.controller.start_new_game(size, mode)

        # Re-apply letter choices to the new game object
        self.set_letter("Blue", self.blue_letter.get())
        self.set_letter("Red", self.red_letter.get())

        # Rebuild GUI board (This will use the initial board_update_callback)
        self.board_frame.size = size
        self.board_frame.build_board()
        self.update_turn_label()

    def set_letter(self, color, letter):
        # Sets the letter choice for the specified player in the current game instance.
        if color == "Blue":
            self.controller.set_player_letter(color, letter)
        else:
            self.controller.set_player_letter(color, letter)

    def update_turn_label(self):
        # Updates the label with the current game status (Turn or Winner/Score).
        status = self.controller.get_game_status()
        self.turn_label.config(text=status)


if __name__ == "__main__":
    app = SOSApp()
    app.mainloop()