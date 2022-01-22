import pygame

import constants as cn
from tile import Tile
from graphic_utils import create_text
from board_utils import point_on_screen


class Deck:
    def __init__(self, dimensions):
        self.dims = dimensions
        self.x, self.y, self.width, self.height = self.dims
        self.width /= cn.MAX_LETTERS

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

    def select_tile(self, index=None):
        for i in self.letters:
            i.selected = False
        if index or index == 0:
            self.letters[index].selected = True

    def parse_key_presses(self, event, board):
        letter_values = self.get_values()
        end = cn.MAX_LETTERS - 1
        empty_tile_index = letter_values.index('') if '' in letter_values else 'end'

        if not event or event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_RETURN:
            if not self.setting_letters:
                self.setting_letters = True
                arg = end if empty_tile_index == 'end' else empty_tile_index
                arg = 0 if not empty_tile_index else arg
                self.select_tile(arg)
            else:
                self.setting_letters = False
                self.select_tile()
            return

        key = str(pygame.key.name(event.key))

        # letter changing
        if self.setting_letters:
            pos = 0
            if isinstance(key, str) and len(key) == 1:
                pos = empty_tile_index if empty_tile_index != 'end' else end
                self.letters[pos].set_letter(key)
            elif empty_tile_index:
                pos = empty_tile_index-1 if empty_tile_index != 'end' else end
                self.letters[pos].set_letter('')
            self.select_tile(pos)
            # self.save_board()

        elif key in 'abcdefghijklmnopqrstuvwxyz':  # letter or delete
            board.set_tile(key)
            next_x, next_y = tuple(map(sum, zip(board.selected_tile, board.travel_direction)))
            if point_on_screen((next_x, next_y)):
                board.selected_tile = (next_x, next_y)
                board.select_tile(next_x, next_y)

                # self.save_board()

        elif key in {'backspace', 'delete'}:
            reverse_travel_direction = (board.travel_direction[0] * -1, board.travel_direction[1] * -1)
            next_x, next_y = tuple(map(sum, zip(board.selected_tile, reverse_travel_direction)))
            if next_x >= 0 and next_y >= 0:
                board.set_tile('')
                board.selected_tile = (next_x, next_y)
                board.select_tile(next_x, next_y)



    def get_values(self):
        return [i.letter for i in self.letters]
