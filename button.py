import pygame
import constants as cn
import time

class Button:
    def __init__(self, dimensions, text, text_color, font_size, bg, function):
        self.dims = dimensions
        self.x, self.y, self.width, self.height = self.dims
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.bg = bg
        self.function = function
        self.time_since_last_press = time.time()

    def draw(self, window):
        pygame.draw.rect(window, self.bg, self.dims, 0, 3)

        font = pygame.font.Font('freesansbold.ttf', self.font_size)
        message = font.render(self.text, True, self.text_color)
        textRect = message.get_rect()
        textRect.center = (self.x + self.width / 2, self.y + self.height / 2)
        window.blit(message, textRect)

    def was_clicked(self):
        if cn.clicked:
            if time.time() - self.time_since_last_press < 1:
                return

            mouse_x, mouse_y = cn.mouse_pos
            if mouse_x in range(self.x, self.x + self.width) and mouse_y in range(self.y, self.y + self.height):
                self.function()
                self.time_since_last_press = time.time()
