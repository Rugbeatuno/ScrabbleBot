import pygame

import constants as cn
import numpy as np
from graphic_utils import create_text
from tile import Tile

class Board:
    values = np.array([['' for x in range(cn.COLUMNS)] for y in range(cn.ROWS)], dtype=object)
    tile_dims = cn.BOARD_DIMS // cn.COLUMNS
    bg_colors = {
        cn.NORMAL: (192, 192, 192),
        cn.TRIPLE_WORD_SCORE: (255, 165, 0),
        cn.TRIPLE_LETTER_SCORE: (168, 120, 168),
        cn.DOUBLE_WORD_SCORE: (255, 192, 203),
        cn.DOUBLE_LETTER_SCORE: (173, 216, 230)
    }

    
    def draw(self, window):
        self.draw_tiles(window)
        self.draw_grid(window)

    def draw_grid(self, window):
        for i in range(cn.ROWS + 1):
            x = cn.BOARD_START_X + self.tile_dims * i
            y = cn.BOARD_START_Y + self.tile_dims * i

            pygame.draw.line(window, (0, 0, 0), (cn.BOARD_START_X, y), (cn.BOARD_WIDTH, y))
            pygame.draw.line(window, (0, 0, 0), (x, cn.BOARD_START_Y), (x, cn.BOARD_HEIGHT))

    def draw_background(self, window, col, row):
        color = self.bg_colors[cn.multipliers[row][col]]
        x, y = self.tile_dims * col + cn.BOARD_START_X, self.tile_dims * row + cn.BOARD_START_Y
        pygame.draw.rect(window, color, (x, y, self.tile_dims, self.tile_dims), 0)

    def draw_text(self, window, col, row):
        x_center = cn.BOARD_START_X + self.tile_dims * col + self.tile_dims / 2
        y_center = cn.BOARD_START_Y + self.tile_dims * row + self.tile_dims / 2
        tile_value = self.values[row][col]
        if tile_value:
            create_text(window, (x_center, y_center+3), tile_value.upper(), 25)

            # letter points
            points = str(cn.LETTER_POINTS[tile_value])
            x_center = self.tile_dims * (col + 1) + cn.BOARD_START_X - 5
            y_center = self.tile_dims * (row + 1) + cn.BOARD_START_Y - 5
            create_text(window, (x_center, y_center), points, 10)

    def draw_tiles(self, window):
        for y in range(cn.ROWS):
            for x in range(cn.COLUMNS):
                self.draw_background(window, x, y)
                self.draw_text(window, x, y)
