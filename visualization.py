import pygame
pygame.display.set_caption('Scrabble Bot')

import constants as cn
from scrabble import Board, Tile
import word

class Visualization:
    def __init__(self):
        self.board = Board()
        self.display = pygame.display.set_mode((cn.BOARD_WIDTH, cn.BOARD_HEIGHT))
        self.selected_tile = (0, 0)  # x, y
        self.travel_direction = (1, 0)
        self.letters = []
        self.best_moves = []
        self.setting_letters = False



    # draw colored squares
    # draw the grid
    # draw selected tile
    # draw letters
    def refresh(self):
        self.display.fill(Tile.bg_colors[cn.NORMAL])
        self.board.draw(self.display)

        word.invalid_board_state(self.board.get_value_only_board())

        self.draw_selected_tile()
        self.draw_travel_direction()
        self.draw_deck()
        self.draw_board_score()
        self.draw_board_validity()
        self.draw_high_scoring_words()
        self.draw_board_indexes()

    def draw_selected_tile(self):
        x, y = self.selected_tile
        pygame.draw.rect(self.display, (50, 120, 0), (x * Tile.width + cn.START_X, y * Tile.width + cn.START_Y, Tile.width,  Tile.width), 5)

    def draw_travel_direction(self):
        new_x, new_y = tuple(map(sum, zip(self.selected_tile, self.travel_direction)))
        buffer = 12
        pygame.draw.rect(self.display, (0, 0, 200), (new_x * Tile.width + buffer + cn.START_X, new_y * Tile.width + cn.START_Y + buffer, Tile.width - buffer * 2, Tile.width - buffer * 2), 3)

    def draw_deck(self):
        uppercase = [i.upper() for i in self.letters]
        text = f'Deck{"(edit)" if self.setting_letters else ""}: {" ".join(uppercase)}'
        message = cn.font.render(text, True, (0, 0, 0))
        self.display.blit(message, (10, 10))

    def draw_board_score(self):
        text = f'Score: {word.calculate_entire_board_score(self.board.get_value_only_board())}'
        message = cn.font.render(text, True, (0, 0, 0))
        self.display.blit(message, (10, 50))

    def draw_board_validity(self):
        invalid = word.invalid_board_state(self.board.get_value_only_board())
        if invalid:
            errors = ['Board Invalid:', *[f'{i[0]} - {i[1]} ({"H" if i[2] == word.HORIZONTAL else "V"})' for i in invalid]]
            for index, i in enumerate(errors):
                text = i
                message = cn.small_font.render(text, True, (200, 20, 20))
                self.display.blit(message, (cn.BOARD_WIDTH - 150, 10 + (index * 10)))

    def draw_board_indexes(self):
        for x in range(cn.COLUMNS):
            x_pos = int(cn.START_X + x * Tile.width + Tile.width / 2)
            y_pos = cn.START_Y - 10
            message = cn.small_font.render(str(x), True, (0, 0, 0))
            textRect = message.get_rect()
            textRect.center = (x_pos, y_pos)
            self.display.blit(message, textRect)
        for y in range(cn.ROWS):
            x_pos = cn.START_X - 10
            y_pos = int(cn.START_Y + y * Tile.width + Tile.width / 2)
            message = cn.small_font.render(str(y), True, (0, 0, 0))
            textRect = message.get_rect()
            textRect.center = (x_pos, y_pos)
            self.display.blit(message, textRect)

    def draw_high_scoring_words(self):
        if self.best_moves:
            options = ['High Scoring Moves:', *[f'{i[0]} - {i[1]} ({"H" if i[2] == word.HORIZONTAL else "V"}) ({i[3]}) {"*" if i[4] else ""}' for i in self.best_moves[-15:]]]
            for index, i in enumerate(options):
                text = i
                message = cn.small_font.render(text, True, (20, 80, 20))
                self.display.blit(message, (cn.BOARD_WIDTH - 300, 10 + (index * 10)))

    def get_selected_tile(self, pos):
        x, y = pos
        new_x, new_y = ((x - cn.START_X) // Tile.width, (y - cn.START_Y) // Tile.width)
        if new_x >= 0 and new_y >= 0:
            self.selected_tile = (int(new_x), int(new_y))

    def get_pressed_key(self, event):
        if event not in cn.KEYS:
            return

        x, y = self.selected_tile
        new_value = cn.KEYS[event]

        if new_value == 'input':
            self.setting_letters = not self.setting_letters
            if not self.setting_letters:
                self.best_moves = word.find_best_move(self.board.get_value_only_board(), self.letters)
            return

        # letter changing
        if self.setting_letters:
            if new_value:
                self.letters.append(new_value)
            elif self.letters:
                self.letters = self.letters[:-1]
            return

        self.board.values[y][x].value = new_value
        if new_value:  # not delete or backspace
            next_x, next_y = tuple(map(sum, zip(self.selected_tile, self.travel_direction)))
            if next_x <= cn.COLUMNS-1 and next_y <= cn.ROWS - 1:
                self.selected_tile = (next_x, next_y)

        # we will want to travel in the opposite direction
        # therefore we will reveres the travel direction
        else:
            reverse_travel_direction = (self.travel_direction[0] * -1, self.travel_direction[1] * -1)
            next_x, next_y = tuple(map(sum, zip(self.selected_tile, reverse_travel_direction)))
            if next_x >= 0 and next_y >= 0:
                self.selected_tile = (next_x, next_y)

    def change_travel_direction(self):
        self.travel_direction = self.travel_direction[::-1]





