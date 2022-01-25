import pygame

import board_utils
import constants as cn
import numpy as np
from graphic_utils import create_text
from tile import Tile


class Board:
    bg_colors = {
        cn.NORMAL: (192, 192, 192),
        cn.TRIPLE_WORD_SCORE: (255, 165, 0),
        cn.TRIPLE_LETTER_SCORE: (168, 120, 168),
        cn.DOUBLE_WORD_SCORE: (255, 192, 203),
        cn.DOUBLE_LETTER_SCORE: (173, 216, 230)
    }

    def __init__(self):
        self.tile_dims = cn.BOARD_DIMS // cn.COLUMNS
        self.values = np.array([[
            Tile(
                (x * self.tile_dims + cn.BOARD_START_X, y * self.tile_dims + cn.BOARD_START_Y, self.tile_dims, self.tile_dims),
                self.bg_colors[cn.multipliers[y][x]],
                ''
            ) for x in range(cn.COLUMNS)] for y in range(cn.ROWS)], dtype=object)

        self.selected_tile = (0, 0)  # x, y
        self.travel_direction = (1, 0)

    def update(self, window):
        self.update_tiles(window)
        self.select_tile()
        self.draw_grid(window)
        self.draw_travel_direction(window)

    def draw_grid(self, window):
        for i in range(cn.ROWS + 1):
            x = cn.BOARD_START_X + self.tile_dims * i
            y = cn.BOARD_START_Y + self.tile_dims * i

            pygame.draw.line(window, (0, 0, 0), (cn.BOARD_START_X, y), (cn.BOARD_WIDTH, y))
            pygame.draw.line(window, (0, 0, 0), (x, cn.BOARD_START_Y), (x, cn.BOARD_HEIGHT))

    def update_tiles(self, window):
        for y in range(cn.ROWS):
            for x in range(cn.COLUMNS):
                tile = self.values[y][x]
                tile.update(window)

    def draw_travel_direction(self, window):
        new_x, new_y = map(sum, zip(self.selected_tile, self.travel_direction))

        buffer = 12
        pygame.draw.rect(window, (0, 0, 200), (
            new_x * self.tile_dims + buffer + cn.BOARD_START_X, new_y * self.tile_dims + cn.BOARD_START_Y + buffer,
            self.tile_dims - buffer * 2, self.tile_dims - buffer * 2), 3)

    def change_travel_direction(self):
        self.travel_direction = self.travel_direction[::-1]

    def select_tile(self, new_x=None, new_y=None):
        if cn.clicked:
            x, y = cn.mouse_pos
            new_x, new_y = (x - cn.BOARD_START_X) // self.tile_dims, (y - cn.BOARD_START_Y) // self.tile_dims

        if new_x is None and new_y is None:
            return
        if board_utils.point_on_screen((new_x, new_y)):
            self.selected_tile = (int(new_x), int(new_y))
            for y in range(cn.ROWS):
                for x in range(cn.COLUMNS):
                    self.values[y][x].selected = False
            self.values[new_y][new_x].selected = True

    def set_tile(self, key):
        x, y = self.selected_tile
        self.values[y][x].set_letter(key)

    def get_values(self):
        return [[self.values[y][x].get_letter() for x in range(cn.COLUMNS)] for y in range(cn.ROWS)]

    @classmethod
    def get_tile_dims(cls):
        return cn.BOARD_DIMS // cn.COLUMNS
