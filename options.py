import time

import pygame
from graphic_utils import create_text
from button import Button
import constants as cn

def nothing():
    pass


class Options:
    buffer = 3
    spacing = 25

    def __init__(self, dimensions):
        self.dims = dimensions
        self.x, self.y, self.width, self.height = self.dims

        self.possible_moves = []
        self.move_buttons = []

        self.current_surface = None
        self.scroll_y = 0
        self.max_y = 0

    def update(self, window, event):
        self.draw(window)
        self.update_scroll_state(event)
        self.update_buttons(window)

    def draw(self, window):
        pygame.draw.rect(window, cn.BG, (self.x, 0, self.width, self.y), 0)
        pygame.draw.rect(window, cn.BG, (self.x, self.y + self.height, self.width, cn.SCREEN_HEIGHT), 0)
        # pygame.draw.rect(window, (180, 180, 180), self.dims, 0, 2)  # option area
        pygame.draw.rect(window, (0, 0, 0), self.dims, 1)  # black frame
        text = ''.join(
            i.ljust(Options.spacing - 1)
            for i in ['#', 'Word', 'Position', 'Direction', 'Bingo', 'Total Score']
        )

        x_center = self.x + self.width / 2
        y_center = self.y - 10
        create_text(window, (x_center, y_center), text, 10)

    def create_buttons(self):
        height = 40
        width = self.width - Options.buffer * 4

        for index, i in enumerate(self.possible_moves[::-1]):
            x = self.buffer
            y = index * height + self.buffer * index + self.buffer * 2

            text = ''
            for i in [f'{index+1}.', i.word, i.pos, i.get_string_dir(), i.get_string_bingo(), i.score]:
                i = str(i)
                text += i.ljust(Options.spacing)

            option = Button(
                (x, y, width, height),
                text,
                (0, 0, 0),
                10,
                (165, 165, 165),
                nothing
            )
            self.move_buttons.append(option)
        self.max_y = len(self.possible_moves) * height

    def update_buttons(self, window):
        if not self.current_surface:
            return
        window.blit(self.current_surface, (self.x + self.buffer, self.scroll_y + self.y))
        self.draw(window)

    def create_surface(self):
        surface = pygame.Surface((self.width - self.buffer * 2, self.max_y)).convert_alpha()
        surface.fill((180, 180, 180))
        for i in self.move_buttons:
            i.draw(surface)
            i.was_clicked()
        self.current_surface = surface

    def update_scroll_state(self, event):
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # scroll down
                self.scroll_y = min(self.scroll_y + 30, 0)
            elif event.button == 5:
                self.scroll_y = max(self.scroll_y - 30, -1 * self.max_y)

    def set_possible_moves(self, moves: list):
        self.possible_moves = moves
        self.create_buttons()
        self.create_surface()
        self.scroll_y = 0
