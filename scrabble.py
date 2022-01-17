import pygame

import constants as cn
import numpy as np

class Board:
    values = [['' for x in range(cn.COLUMNS)] for y in range(cn.ROWS)]
    values = np.array(values, dtype='<U1')

    tile_width = int((cn.BOARD_WIDTH - cn.START_X) // cn.COLUMNS)
    tile_height = int((cn.BOARD_HEIGHT - cn.START_Y) // cn.COLUMNS)

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
        for i in range(cn.ROWS):
            x = cn.START_X + self.tile_width * i
            y = cn.START_Y + self.tile_width * i
            pygame.draw.line(window, (0, 0, 0), (cn.START_X, y), (cn.BOARD_WIDTH, y))
            pygame.draw.line(window, (0, 0, 0), (x, cn.START_Y), (x, cn.BOARD_HEIGHT))

    def draw_tiles(self, window):
        for y in range(cn.ROWS):
            for x in range(cn.COLUMNS):
                self.draw_background(window, x, y)
                self.draw_text(window, x, y)

    def draw_background(self, window, col, row):
        color = self.bg_colors[cn.multipliers[row][col]]
        x, y = self.tile_width * col + cn.START_X, self.tile_height * row + cn.START_Y
        pygame.draw.rect(window, color, (x, y, self.tile_width, self.tile_width), 0)

    def draw_text(self, window, col, row):
        x_center = cn.START_X + self.tile_width * col + self.tile_width / 2
        y_center = cn.START_Y + self.tile_height * row + self.tile_height / 2
        tile_value = self.values[row][col]
        if tile_value:
            letter = cn.font.render(tile_value.upper(), True, (0, 0, 0))
            textRect = letter.get_rect()
            textRect.center = (x_center, y_center + 3)  # fixed offset to account for uppercase letters
            window.blit(letter, textRect)

            # letter points
            points = str(cn.LETTER_POINTS[tile_value])
            letter_points = cn.small_font.render(points, True, (0, 0, 0))
            textRect = letter_points.get_rect()
            textRect.center = (
                self.tile_width * (col + 1) + cn.START_X - 5, self.tile_height * (row + 1) + cn.START_Y - 5)
            window.blit(letter_points, textRect)
