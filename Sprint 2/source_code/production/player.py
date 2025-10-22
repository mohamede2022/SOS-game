class Player:
    def __init__(self, color, is_human=True):
        self.color = color
        self.is_human = is_human
        self.letter_choice = "S"

    def set_letter(self, letter):
        self.letter_choice = letter
