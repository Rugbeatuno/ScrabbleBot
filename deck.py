import pygame

import constants as cn
from graphic_utils import create_text

class Deck:
    def __init__(self, x, y, width, height):
        self.letters = []

        self.x = x
        self.y = y
        self.width = width / cn.MAX_LETTERS
        self.height = height

    def draw(self, window):
        for i in range(cn.MAX_LETTERS):
            x = self.x + self.width * i
            curved_edges = 3 if i in [0, cn.MAX_LETTERS - 1] else 0
            
            pygame.draw.rect(window, (180, 180, 180), (x, self.y, self.width, self.height), 0, curved_edges)
