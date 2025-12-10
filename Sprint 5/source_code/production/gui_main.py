# gui_main.py
import tkinter as tk
from tkinter import filedialog
from controller import GameController
from gui_board import GUIBoard


class SOSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SOS Game")
        self.geometry("750x750")
        self.controller = GameController()
        self.board_frame = None

        # Variables
        self.mode_var = tk.StringVar(value="Simple")
        self.size_var = tk.StringVar(value="3")
        self.blue_type = tk.StringVar(value="Human")
        self.red_type = tk.StringVar(value="Human")
        self.blue_letter = tk.StringVar(value="S")
        self.red_letter = tk.StringVar(value="S")
        # NEW
        self.record_var = tk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10)
        tk.Label(top_frame, text="Game Mode:").grid(row=0, column=0)
        tk.Radiobutton(top_frame, text="Simple", variable=self.mode_var, value="Simple").grid(row=0, column=1)
        tk.Radiobutton(top_frame, text="General", variable=self.mode_var, value="General").grid(row=0, column=2)
        tk.Label(top_frame, text="Size:").grid(row=0, column=3, padx=10)
        tk.Entry(top_frame, textvariable=self.size_var, width=5).grid(row=0, column=4)
        tk.Button(top_frame, text="New Game", command=self.start_new_game).grid(row=0, column=5, padx=10)

        # Player Controls
        p_frame = tk.Frame(self)
        p_frame.pack(pady=10)

        # Blue
        b_frame = tk.LabelFrame(p_frame, text="Blue Player")
        b_frame.grid(row=0, column=0, padx=10)
        tk.Radiobutton(b_frame, text="Human", variable=self.blue_type, value="Human").pack(anchor="w")
        tk.Radiobutton(b_frame, text="Computer", variable=self.blue_type, value="Computer").pack(anchor="w")
        tk.Radiobutton(b_frame, text="S", variable=self.blue_letter, value="S",
                       command=lambda: self.set_letter("Blue", "S")).pack(anchor="w")
        tk.Radiobutton(b_frame, text="O", variable=self.blue_letter, value="O",
                       command=lambda: self.set_letter("Blue", "O")).pack(anchor="w")

        # Red
        r_frame = tk.LabelFrame(p_frame, text="Red Player")
        r_frame.grid(row=0, column=1, padx=10)
        tk.Radiobutton(r_frame, text="Human", variable=self.red_type, value="Human").pack(anchor="w")
        tk.Radiobutton(r_frame, text="Computer", variable=self.red_type, value="Computer").pack(anchor="w")
        tk.Radiobutton(r_frame, text="S", variable=self.red_letter, value="S",
                       command=lambda: self.set_letter("Red", "S")).pack(anchor="w")
        tk.Radiobutton(r_frame, text="O", variable=self.red_letter, value="O",
                       command=lambda: self.set_letter("Red", "O")).pack(anchor="w")

        # Replay/Record Controls
        rec_frame = tk.LabelFrame(p_frame, text="Recording")
        rec_frame.grid(row=0, column=2, padx=10, sticky="n")
        tk.Checkbutton(rec_frame, text="Record Game", variable=self.record_var, command=self.toggle_record).pack(
            anchor="w")
        tk.Button(rec_frame, text="Replay From File", command=self.load_replay).pack(pady=2)
        self.next_btn = tk.Button(rec_frame, text="Next Move (Replay)", command=self.next_replay_move,
                                  state=tk.DISABLED)
        self.next_btn.pack(pady=2)

        self.turn_label = tk.Label(self, text="Start a New Game", font=("Arial", 14))
        self.turn_label.pack(pady=5)

        self.board_container = tk.Frame(self)
        self.board_container.pack()
        self.board_frame = GUIBoard(self.board_container, self.controller, board_update_callback=self.update_ui)
        self.board_frame.pack()

    def start_new_game(self):
        try:
            size = int(self.size_var.get())
        except:
            return

        self.controller.start_new_game(size, self.mode_var.get(), self.blue_type.get(), self.red_type.get())
        self.controller.is_recording = self.record_var.get()
        self.set_letter("Blue", self.blue_letter.get())
        self.set_letter("Red", self.red_letter.get())

        if self.board_frame: self.board_frame.destroy()
        self.board_frame = GUIBoard(self.board_container, self.controller, size, self.update_ui)
        self.board_frame.pack()

        self.next_btn.config(state=tk.DISABLED)
        self.update_ui()
        self.check_computer_move()

    def set_letter(self, color, letter):
        self.controller.set_player_letter(color, letter)

    def toggle_record(self):
        self.controller.is_recording = self.record_var.get()

    def load_replay(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filename and self.controller.load_game_from_file(filename):
            self.board_frame.destroy()
            self.board_frame = GUIBoard(self.board_container, self.controller, self.controller.game.board.size,
                                        self.update_ui)
            self.board_frame.pack()
            self.board_frame.disable_board()  # Replay is read-only
            self.next_btn.config(state=tk.NORMAL)
            self.update_ui()

    def next_replay_move(self):
        if self.controller.get_next_replay_move():
            self.board_frame.update_board_display()
            self.update_ui()
        else:
            self.next_btn.config(state=tk.DISABLED)
            self.turn_label.config(text="Replay Finished")

    def update_ui(self):
        status = self.controller.get_game_status()
        self.turn_label.config(text=status)

        # Auto-save if recording and game over
        if self.controller.game.is_game_over() and self.controller.is_recording:
            self.controller.record_game_to_file("game_recording.txt")
            self.turn_label.config(text=status + " (Saved to game_recording.txt)")
            self.controller.is_recording = False
            self.record_var.set(False)

        if not self.controller.game.is_game_over():
            self.check_computer_move()

    def check_computer_move(self):
        if self.controller.is_current_player_computer() and not self.controller.is_replaying:
            self.board_frame.disable_board()
            self.after(500, self.perform_computer_move)
        elif not self.controller.is_replaying:
            self.board_frame.enable_board()

    def perform_computer_move(self):
        if self.controller.handle_computer_move() != (-1, -1, ""):
            self.board_frame.update_board_display()
            self.update_ui()

    def update_game_status(self):
        winner_color_name = self.controller.get_winner_color()  # Get the color string from the controller
        status_message = self.controller.get_game_status()  # Get the full status message

        # --- New Color Logic ---
        if winner_color_name:
            # Game is over. Set background to winner's color.
            # Use HTML/Tkinter-friendly color names
            if winner_color_name == "Blue":
                bg_color = "RoyalBlue"
                fg_color = "white"
            elif winner_color_name == "Red":
                bg_color = "red"
                fg_color = "white"
            else:  # Draw or Gray
                bg_color = "light gray"
                fg_color = "black"

            # Apply the color and update the text
            self.status_label.config(bg=bg_color, fg=fg_color)
            self.status_label_text.set(status_message)

        else:
            # Game is in progress. Reset to default colors.
            self.status_label.config(bg="white", fg="black")
            self.status_label_text.set(status_message)


if __name__ == "__main__":
    app = SOSApp()
    app.mainloop()