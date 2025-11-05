
class Player:
    def __init__(self, color, is_human=True):
        self.color = color
        self.is_human = is_human
        self.letter_choice = "S"
        self.score = 0  # Initialize the score attribute

    def set_letter(self, letter):
        self.letter_choice = letter