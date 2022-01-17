
from constants import HORIZONTAL, VERTICAL

class Word:
    def __init__(self, word, start_pos, direction, score, bingo, algorithm):
        self.word = word
        self.pos = start_pos
        self.dir = direction
        self.score = score
        self.was_bingo = bingo
        self.alg = algorithm


    def get_length(self):
        return len(self.word)

    def get_string_dir(self):
        return 'H' if self.dir == HORIZONTAL else 'V'
