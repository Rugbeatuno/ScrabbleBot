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
            ''
        ) for i in range(cn.MAX_LETTERS)]


    def draw(self, window):
        for i in self.letters:
            i.update(window)

        # for i in range(cn.MAX_LETTERS):
        #     x = self.x + self.width * i
        #     curved_edges = 3 if i in [0, cn.MAX_LETTERS - 1] else 0


