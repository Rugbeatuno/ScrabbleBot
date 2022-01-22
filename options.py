import pygame
from graphic_utils import create_text
from button import Button

def nothing():
    pass


class Options:
    buffer = 2
    def __init__(self, dimensions):
        self.dims = dimensions
        self.x, self.y, self.width, self.height = self.dims

        self.possible_moves = []
        self.move_buttons = []

    def update(self, window, event):
        self.draw(window)

    def draw(self, window):
        pygame.draw.rect(window, (180, 180, 180), self.dims, 0, 2)  # option area
        pygame.draw.rect(window, (0, 0, 0), self.dims, 2, 2)  # black frame
        string = 'Word                            Dir                       Bingo                       Total Score'
        x_center = self.x + self.width / 2
        y_center = self.y - 10
        create_text(window, (x_center, y_center), string, 10)

    def create_buttons(self):
        height = 40
        width = self.width - Options.buffer * 2

        for index, i in enumerate(self.possible_moves):
            x = self.buffer
            y = index * height + self.buffer
            option = Button(
                (x, y, width, height),
                f'{i["word"]}         {i["dir"]}      {i["was_bingo"]}         {i["score"]}',
                (0, 0, 0),
                10,
                (130, 130, 130),
                nothing
            )


