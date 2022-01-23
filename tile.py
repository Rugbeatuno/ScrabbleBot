import pygame

import constants as cn
from graphic_utils import create_text


class Tile:
    def __init__(self, dimensions, bg_color, letter):
        self.dims = dimensions
        self.x, self.y, self.width, self.height = self.dims
        self.bg = bg_color

        self.letter = letter
        self.points = cn.LETTER_POINTS[self.letter] if letter else 0

        self.letter_font_size = int(self.width * 0.7)
        self.points_font_size = int(self.width * 0.25)

        self.selected = False

    def update(self, window):
        self.draw(window)

    def draw(self, window):
        pygame.draw.rect(window, self.bg, self.dims, 0)
        if self.selected:
            pygame.draw.rect(window, (50, 120, 0), self.dims, 5, 3)
        if not self.letter:
            return
        # main letter
        x_center = self.x + self.width / 2
        y_center = self.y + self.height / 2
        create_text(window, (x_center, y_center+2), self.letter.upper(), self.letter_font_size)
        # letter score
        x_center = self.x + self.width - (self.width * 0.15)
        y_center = self.y + self.height - (self.height * 0.15)
        create_text(window, (x_center, y_center), self.points, self.points_font_size)

    def set_letter(self, new_letter):
        if new_letter in 'abcdefghijklmnopqrstuvwxyz':
            self.letter = new_letter
            self.points = cn.LETTER_POINTS[self.letter] if self.letter else 0

    def get_letter(self):
        return self.letter

    def get_points(self):
        return self.points

