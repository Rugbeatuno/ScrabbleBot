import pygame
import constants as cn
import time

from graphic_utils import create_text

class Button:
    def __init__(
            self,
            dimensions,
            text,
            text_color,
            font_size,
            bg,
            on_hover=None,
            args1=None,
            on_click=None,
            args2=None,
            absolute_pos=()
    ):
        self.dims = dimensions
        self.x, self.y, self.width, self.height = self.dims
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.bg = bg

        self.on_hover = on_hover
        self.on_click = on_click
        self.args1 = args1
        self.args2 = args1
        self.absolute_pos = absolute_pos

        self.time_since_last_press = time.time()


    def update(self, window):
        self.draw(window)

    def draw(self, window):
        pygame.draw.rect(window, self.bg, self.dims, 0, 3)

        pos = (self.x + self.width / 2, self.y + self.height / 2)
        create_text(window, pos, self.text, self.font_size, self.text_color)

    def is_hovering(self, scroll_y):
        mouse_x, mouse_y = cn.mouse_pos
        if self.absolute_pos:
            x_range = range(self.absolute_pos[0], self.absolute_pos[0] + self.width)
            y_range = range(self.absolute_pos[1] + scroll_y, self.absolute_pos[1] + scroll_y + self.height)
        else:
            x_range = range(self.x, self.x + self.width)
            y_range = range(self.y, self.y + self.height)

        return mouse_x in x_range and mouse_y in y_range

    def actions(self, scroll_y):
        if self.is_hovering(scroll_y):
            if self.on_hover:
                self.on_hover(self.args1) if self.args1 else self.on_hover()

            if self.on_click and cn.clicked:
                if time.time() - self.time_since_last_press < 0.5:
                    return

                cn.clicked = None
                self.time_since_last_press = time.time()
