import pygame

import constants as cn


class Tile:
    bg_colors = {
        cn.NORMAL: (192, 192, 192),
        cn.TRIPLE_WORD_SCORE: (255, 165, 0),
        cn.TRIPLE_LETTER_SCORE: (168, 120, 168),
        cn.DOUBLE_WORD_SCORE: (255, 192, 203),
        cn.DOUBLE_LETTER_SCORE: (173, 216, 230)
    }

    width = int((cn.BOARD_WIDTH - cn.START_X) // cn.COLUMNS)
    height = int((cn.BOARD_HEIGHT - cn.START_Y) // cn.COLUMNS)

    def __init__(self, row, column, value):
        self.row = row
        self.col = column
        self.value = value
        self.is_selected = False

    def draw(self, window):
        self.draw_background(window)
        self.draw_text(window)

    def draw_background(self, window):
        color = self.bg_colors[cn.multipliers[self.row][self.col]]
        x, y = self.width * self.col + cn.START_X, self.height * self.row + cn.START_Y
        pygame.draw.rect(window, color, (x, y, self.width, self.width), 0)

    def draw_text(self, window):
        x_center = cn.START_X + self.width * self.col + self.width / 2
        y_center = cn.START_Y + self.height * self.row + self.height / 2
        tile = Board.values[self.row][self.col]
        tile_value = tile.value
        if tile_value:
            letter = cn.font.render(tile_value.upper(), True, (0, 0, 0))
            textRect = letter.get_rect()
            textRect.center = (x_center, y_center + 3)  # fixed offset to account for uppercase letters
            window.blit(letter, textRect)

            # letter points
            points = str(cn.LETTER_POINTS[tile_value])
            letter_points = cn.small_font.render(points, True, (0, 0, 0))
            textRect = letter_points.get_rect()
            textRect.center = (self.width * (self.col + 1) + cn.START_X - 5, self.height * (self.row + 1) + cn.START_Y - 5)
            window.blit(letter_points, textRect)



class Board:
    values = board_values = [[Tile(y, x, '') for x in range(cn.COLUMNS)] for y in range(cn.ROWS)]

    def draw(self, window):
        self.draw_tiles(window)
        self.draw_grid(window)

    def draw_grid(self, window):
        for i in range(cn.ROWS):
            x = cn.START_X + Tile.width * i
            y = cn.START_Y + Tile.height * i
            pygame.draw.line(window, (0, 0, 0), (cn.START_X, y), (cn.BOARD_WIDTH, y))
            pygame.draw.line(window, (0, 0, 0), (x, cn.START_Y), (x, cn.BOARD_HEIGHT))

    def draw_tiles(self, window):
        for y in range(cn.ROWS):
            for x in range(cn.COLUMNS):
                Board.values[y][x].draw(window)

    def get_value_only_board(self):
        return [[self.values[j][i].value for i in range(cn.COLUMNS)] for j in range(cn.ROWS)]

