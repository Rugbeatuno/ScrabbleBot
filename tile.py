import pygame

import constants as cn
from graphic_utils import create_text


class Tile:
    def __init__(self, dimensions, bg_color, letter):
        self.dims = dimensions
        self.x, self.y, self.width, self.height = self.dims
        self.bg = bg_color
        self.letter = letter
        self.points = cn.LETTER_POINTS[self.letter]

        self.letter_font_size = int(self.width * 0.75)
        self.points_font_size = int(self.width * 0.2)

    def draw(self, window):
        pygame.draw.rect(window, self.bg, self.dims, 0)

        # main letter
        x_center = self.x + self.width / 2
        y_center = self.y + self.height / 2
        create_text(window, (x_center, y_center), self.letter, self.letter_font_size)

        # letter score
        x_center = self.x + self.width - 5
        y_center = self.y + self.height - 5
        create_text(window, (x_center, y_center), self.points, self.points_font_size)

    def get_letter(self):
        return self.letter

    def get_points(self):
        return self.points
