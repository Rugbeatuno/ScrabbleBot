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

    def update(self, window, event, board_obj):
        self.parse_key_presses(event, board_obj)
        self.draw(window)

    def draw(self, window):
        for i in self.letters:
            i.update(window)

    def parse_key_presses(self, event, board):
        if event and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.setting_letters = not self.setting_letters
                if not self.setting_letters:
                    # self.best_moves = algorithms.find_best_move(self.board.get_values(), self.letters)
                    # self.preview_index = None
                    pass
                return

            key = cn.KEYS[event.key]

            # letter changing
            if self.setting_letters:
                letter_values = self.get_values()
                end = cn.MAX_LETTERS - 1
                empty_tile_index = letter_values.index('') if '' in letter_values else 'end'

                if isinstance(key, str) and len(key) == 1:
                    pos = empty_tile_index if empty_tile_index != 'end' else end
                    self.letters[pos].set_letter(key)
                elif empty_tile_index:
                    pos = empty_tile_index-1 if empty_tile_index != 'end' else end
                    self.letters[pos].set_letter('')

                # self.save_board()
                return

            # typing on board
            elif isinstance(key, str) or not key:  # letter or delete
                if not key:  # not delete or backspace
                    next_x, next_y = tuple(map(sum, zip(self.board.selected_tile, self.board.travel_direction)))
                    if next_x <= cn.COLUMNS - 1 and next_y <= cn.ROWS - 1:
                        self.board.selected_tile = (next_x, next_y)
                board.set_tile(key)
            # self.save_board()


            else:
                reverse_travel_direction = (self.board.travel_direction[0] * -1, self.board.travel_direction[1] * -1)
                next_x, next_y = tuple(map(sum, zip(self.board.selected_tile, reverse_travel_direction)))
                if next_x >= 0 and next_y >= 0:
                    self.board.selected_tile = (next_x, next_y)


    def get_values(self):
        return [i.letter for i in self.letters]
