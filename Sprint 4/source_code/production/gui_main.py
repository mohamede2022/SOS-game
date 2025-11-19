# gui_main.py (Updated for Sprint 4)
import tkinter as tk
from tkinter import messagebox
from controller import GameController
from gui_board import GUIBoard


class SOSApp(tk.Tk):
    # Initialize the main app
    def __init__(self):
        super().__init__()
        self.title("SOS Game")
        self.geometry("750x700")

        self.controller = GameController()
        self.board_frame = None
        self.turn_label = None

        # Game Settings Variables
        self.mode_var = tk.StringVar(value="Simple")
        self.size_var = tk.StringVar(value="3")

        # Player Type Variables (NEW)
        self.blue_type = tk.StringVar(value="Human")
        self.red_type = tk.StringVar(value="Human")

        # Player Letter Variables (Existing)
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

        tk.Button(top_frame, text="New Game", command=self.start_new_game).grid(row=0, column=5, padx=20)

        # Player Control Frame
        player_control_frame = tk.Frame(self)
        player_control_frame.pack(pady=10)

        # Blue Player Controls
        blue_frame = tk.LabelFrame(player_control_frame, text="Blue Player", padx=10, pady=5)
        blue_frame.grid(row=0, column=0, padx=20, sticky="n")

        # Blue Player Type (Human/Computer)
        tk.Label(blue_frame, text="Type:").pack(anchor="w")
        tk.Radiobutton(blue_frame, text="Human", variable=self.blue_type, value="Human").pack(anchor="w")
        tk.Radiobutton(blue_frame, text="Computer", variable=self.blue_type, value="Computer").pack(anchor="w")

        # Blue Player Letter
        tk.Label(blue_frame, text="Letter:").pack(pady=(5, 0), anchor="w")
        tk.Radiobutton(blue_frame, text="S", variable=self.blue_letter, value="S",
                       command=lambda: self.set_letter("Blue", "S")).pack(anchor="w")
        tk.Radiobutton(blue_frame, text="O", variable=self.blue_letter, value="O",
                       command=lambda: self.set_letter("Blue", "O")).pack(anchor="w")

        # Red Player Controls
        red_frame = tk.LabelFrame(player_control_frame, text="Red Player", padx=10, pady=5)
        red_frame.grid(row=0, column=1, padx=20, sticky="n")

        # Red Player Type (Human/Computer)
        tk.Label(red_frame, text="Type:").pack(anchor="w")
        tk.Radiobutton(red_frame, text="Human", variable=self.red_type, value="Human").pack(anchor="w")
        tk.Radiobutton(red_frame, text="Computer", variable=self.red_type, value="Computer").pack(anchor="w")

        # Red Player Letter
        tk.Label(red_frame, text="Letter:").pack(pady=(5, 0), anchor="w")
        tk.Radiobutton(red_frame, text="S", variable=self.red_letter, value="S",
                       command=lambda: self.set_letter("Red", "S")).pack(anchor="w")
        tk.Radiobutton(red_frame, text="O", variable=self.red_letter, value="O",
                       command=lambda: self.set_letter("Red", "O")).pack(anchor="w")

        # Turn Label
        self.turn_label = tk.Label(self, text="Click 'New Game' to start", font=("Arial", 14))
        self.turn_label.pack(pady=10)

        # Game Board Frame
        self.board_frame_container = tk.Frame(self)
        self.board_frame_container.pack()

        # Initial board setup
        self.board_frame = GUIBoard(self.board_frame_container, self.controller, size=3,
                                    board_update_callback=self.update_turn_label)
        self.board_frame.pack()

    def start_new_game(self):
        try:
            size = int(self.size_var.get())
            if size < 3 or size > 10:
                raise ValueError
        except ValueError:
            self.turn_label.config(text="Invalid board size. Must be an integer between 3 and 10.", fg="red")
            return

        mode = self.mode_var.get()
        blue_type = self.blue_type.get()
        red_type = self.red_type.get()

        self.controller.start_new_game(size, mode, blue_type, red_type)

        # Reapply letter choices to the new game object
        self.set_letter("Blue", self.blue_letter.get())
        self.set_letter("Red", self.red_letter.get())

        # Rebuild GUI board
        if self.board_frame:
            self.board_frame.destroy()

        self.board_frame = GUIBoard(self.board_frame_container, self.controller, size=size, board_update_callback=self.update_turn_label)
        self.board_frame.pack()

        self.update_turn_label()

        # Immediately check for a computer move if the starting player is a computer
        self.check_for_computer_move()

    def set_letter(self, color, letter):
        # Sets the letter choice for the specified player in the current game instance.
        self.controller.set_player_letter(color, letter)

    def update_turn_label(self):
        # Updates the label with the current game status (Turn or Winner/Score).
        status = self.controller.get_game_status()
        if self.controller.game.is_game_over():
            fg_color = "green"
        else:
            # Get the color string from the Controller
            player_color_name = self.controller.get_current_turn()
            fg_color = player_color_name.lower()

        self.turn_label.config(text=status, fg=fg_color)

        # After updating the label, check if the next move should be a computer's move
        if not self.controller.game.is_game_over():
            self.check_for_computer_move()

    def check_for_computer_move(self):
        # Checks if it's the computer's turn and triggers the move after a delay.
        if self.controller.is_current_player_computer() and not self.controller.game.is_game_over():
            # Disable human interaction during computer's turn
            self.board_frame.disable_board()
            self.after(500, self.perform_computer_move)

    def perform_computer_move(self):
        # Executes the computer's move, updates the GUI, and checks if the computer retained turn.
        player_who_moved = self.controller.game.current_turn
        r, c, letter = self.controller.handle_computer_move()

        # Update the GUI board
        if r != -1:
            color = "blue" if player_who_moved.color == "Blue" else "red"
            self.board_frame.cells[r][c].config(text=letter, fg=color, state=tk.DISABLED)

        # Update the status label
        self.update_turn_label()

        # Check for next turn
        if self.controller.game.is_game_over():
            self.board_frame.disable_board()
        elif not self.controller.is_current_player_computer():
            # Turn toggled to a human
            self.board_frame.enable_board()
        else:
            # The computer scored and retained turn so it calls itself again
            self.check_for_computer_move()


if __name__ == "__main__":
    app = SOSApp()
    app.mainloop()