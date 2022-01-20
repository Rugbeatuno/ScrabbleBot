import pygame

import constants as cn
from tile import Tile
from graphic_utils import create_text


class Deck:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width / cn.MAX_LETTERS
        self.height = height

        self.letters = [Tile(
            (self.x + self.width * i + i, self.y, self.width, self.height),
            (180, 180, 180),
            '',
        ) for i in range(cn.MAX_LETTERS)]

        self.setting_letters = False

    def update(self, window, event):
        pass

    def draw(self, window):
        for i in self.letters:
            i.update(window)

    def parse_key_presses(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.setting_letters = not self.setting_letters
                if not self.setting_letters:
                    # self.best_moves = algorithms.find_best_move(self.board.get_values(), self.letters)
                    # self.preview_index = None
                    pass
                return

                # letter changing
            if self.setting_letters:
                key = cn.KEYS[event]
                letter_values = self.get_values()
                empty_tile_index = letter_values.index('')

                if isinstance(key, str) and len(key) == 1:
                    self.letters[empty_tile_index].letter = key
                elif empty_tile_index:
                    self.letters = self.letters[:-1]
                # self.save_board()
                return


    def get_values(self):
        return [i.letter for i in self.letters]
