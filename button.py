import pygame
import constants as cn
import time

from graphic_utils import create_text

class Button:
    def __init__(self, dimensions, text, text_color, font_size, bg, function, absolute_pos=()):
        self.dims = dimensions
        self.x, self.y, self.width, self.height = self.dims
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.bg = bg
        self.function = function
        self.time_since_last_press = time.time()

        self.absolute_pos = absolute_pos

    def update(self, window):
        self.draw(window)

    def draw(self, window):
        pygame.draw.rect(window, self.bg, self.dims, 0, 3)

        pos = (self.x + self.width / 2, self.y + self.height / 2)
        create_text(window, pos, self.text, self.font_size, self.text_color)

    def was_clicked(self, scroll_y):
        if not cn.clicked:
            return
        if time.time() - self.time_since_last_press < 0.5:
            return

        mouse_x, mouse_y = cn.mouse_pos
        if self.absolute_pos:
            x_range = range(self.absolute_pos[0], self.absolute_pos[0] + self.width)
            y_range = range(self.absolute_pos[1] + scroll_y, self.absolute_pos[1] + scroll_y + self.height)
        else:
            x_range = range(self.x, self.x + self.width)
            y_range = range(self.y, self.y + self.height)

        if mouse_x in x_range and mouse_y in y_range:
            print(self.text, "clicked", self.absolute_pos)
            cn.clicked = None
            self.function()
            self.time_since_last_press = time.time()
