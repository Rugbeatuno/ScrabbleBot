import time

import pygame
from graphic_utils import create_text
from button import Button
import constants as cn
from scrabble import Board

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

        self.window = None

    def update(self, window, event):
        self.window = window
        self.update_scroll_state(event)
        self.draw(window)
        self.update_buttons()

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
        self.move_buttons.clear()

        height = 40
        width = self.width - Options.buffer * 4

        for index, i in enumerate(self.possible_moves[::-1]):
            x = self.buffer
            y = index * height + self.buffer * index + self.buffer * 2

            text = ''
            for item in [f'{index+1}.', i.word, i.pos, i.get_string_dir(), i.get_string_bingo(), i.score]:
                item = str(item)
                text += item.ljust(Options.spacing)

                option = Button(
                    (x, y, width, height),
                    text,
                    (0, 0, 0),
                    10,
                    (165, 165, 165),
                    on_hover=self.preview_word,
                    args1=i,
                    absolute_pos=(self.x + x, self.y + y)
                )
            self.move_buttons.append(option)
        self.max_y = len(self.possible_moves) * height + self.height

    def update_buttons(self):
        if not self.current_surface:
            return

        self.window.blit(self.current_surface, (self.x + self.buffer, self.scroll_y + self.y))
        self.draw(self.window)
        for button in self.move_buttons:
            button.actions(self.scroll_y)

    def create_surface(self):
        surface = pygame.Surface((self.width - self.buffer * 2, self.max_y)).convert_alpha()
        surface.fill((180, 180, 180))
        for button in self.move_buttons:
            button.update(surface)
        self.current_surface = surface


    def preview_word(self, word_obj):
        word = word_obj.word
        dir = word_obj.dir
        length = len(word)
        word_x, word_y = word_obj.pos
        tile_dims = Board.get_tile_dims()
        x = cn.BOARD_START_X + word_x * tile_dims + 1
        y = cn.BOARD_START_Y + word_y * tile_dims + 1
        width = tile_dims * length - 1 if dir == cn.HORIZONTAL else tile_dims - 1
        height = tile_dims * length - 1 if dir == cn.VERTICAL else tile_dims - 1

        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        green = (120, 170, 120, 120)
        surface.fill(green)

        for index, l in enumerate(word):
            half = tile_dims / 2
            center = (half, tile_dims * index + half) if dir == cn.VERTICAL else (tile_dims * index + half, half)
            create_text(surface, center, l.upper(), int(tile_dims * 0.7))
            self.window.blit(surface, (x, y))

    def update_scroll_state(self, event):
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # scroll down
                self.scroll_y = min(self.scroll_y + 25, 0)
            elif event.button == 5:
                self.scroll_y = max(self.scroll_y - 25, -1 * self.max_y)

    def set_possible_moves(self, moves: list):
        self.possible_moves = moves
        self.create_buttons()
        self.create_surface()
        self.scroll_y = 0
