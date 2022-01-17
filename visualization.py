import json

import pygame

import board_utils
import constants
import constants as cn
from scrabble import Board
import algorithms
import board_cycling
from button import Button


pygame.display.set_caption('Scrabble Bot')

class Visualization:
    def __init__(self):
        self.board = Board()
        self.display = pygame.display.set_mode((cn.BOARD_WIDTH, cn.BOARD_HEIGHT))
        self.selected_tile = (0, 0)  # x, y
        self.travel_direction = (1, 0)
        self.letters = []
        self.best_moves = []

        self.setting_letters = False
        self.preview_index = None
        self.total_score = 0
        self.board_number = 1

        self.buttons = [
            Button(10, 80, 100, 50, 'New Board', (0, 0, 0), 15, (144, 240, 144), self.add_board),
            Button(10, 130, 100, 50, 'Delete Board', (0, 0, 0), 12, (240, 144, 144), self.delete_board)
        ]

        with open('boards.json', 'r') as f:
            if not json.load(f):
                self.add_board()
        self.load_board()

    def refresh(self):
        board_utils.invalid_board_state(self.board.values)

        self.display.fill((200, 200, 200))
        self.board.draw(self.display)
        self.refresh_buttons()

        self.draw_board_number()
        self.get_selected_tile()
        self.draw_selected_tile()
        self.draw_travel_direction()
        self.draw_deck()
        self.draw_score()
        self.draw_board_validity()
        self.draw_high_scoring_words()
        self.draw_board_indexes()

    def refresh_buttons(self):
        for button in self.buttons:
            button.draw(self.display)
            button.was_clicked()

    def draw_selected_tile(self):
        x, y = self.selected_tile
        pygame.draw.rect(self.display, (50, 120, 0), (x * Board.tile_width + cn.START_X, y * Board.tile_width + cn.START_Y, Board.tile_width,  Board.tile_width), 5)

    def draw_travel_direction(self):
        new_x, new_y = tuple(map(sum, zip(self.selected_tile, self.travel_direction)))
        buffer = 12
        pygame.draw.rect(self.display, (0, 0, 200), (new_x * Board.tile_width + buffer + cn.START_X, new_y * Board.tile_width + cn.START_Y + buffer, Board.tile_width - buffer * 2, Board.tile_width - buffer * 2), 3)

    def draw_deck(self):
        uppercase = [i.upper() for i in self.letters]
        text = f'Deck{"(edit)" if self.setting_letters else ""}: {" ".join(uppercase)}'
        message = cn.font.render(text, True, (0, 0, 0))
        self.display.blit(message, (10, 10))

    def draw_score(self):
        text = f'Score: {self.total_score}'
        message = cn.font.render(text, True, (0, 0, 0))
        self.display.blit(message, (10, 50))

    def draw_board_number(self):
        boards = board_cycling.get_boards()
        if not boards:
            return
        text = f'Board {self.board_number}/{boards[-1]}'
        message = cn.small_font.render(text, True, (0, 0, 0))
        self.display.blit(message, (cn.BOARD_WIDTH - 60, 10))

    def draw_board_validity(self):
        invalid = board_utils.invalid_board_state(self.board.values)
        if invalid:
            errors = ['Board Invalid:', *[f'{i[0]} - {i[1]} ({"H" if i[2] == constants.HORIZONTAL else "V"})' for i in invalid]]
            for index, i in enumerate(errors):
                text = i
                message = cn.small_font.render(text, True, (200, 20, 20))
                self.display.blit(message, (cn.BOARD_WIDTH - 150, 10 + (index * 10)))

    def draw_board_indexes(self):
        for x in range(cn.COLUMNS):
            x_pos = int(cn.START_X + x * Board.tile_width + Board.tile_width / 2)
            y_pos = cn.START_Y - 10
            message = cn.small_font.render(str(x), True, (0, 0, 0))
            textRect = message.get_rect()
            textRect.center = (x_pos, y_pos)
            self.display.blit(message, textRect)
        for y in range(cn.ROWS):
            x_pos = cn.START_X - 10
            y_pos = int(cn.START_Y + y * Board.tile_width + Board.tile_width / 2)
            message = cn.small_font.render(str(y), True, (0, 0, 0))
            textRect = message.get_rect()
            textRect.center = (x_pos, y_pos)
            self.display.blit(message, textRect)

    def draw_high_scoring_words(self):
        if not self.best_moves:
            return
        options = ['High Scoring Moves:', *[f'{i.word} - {i.pos} ({i.get_string_dir()}) ({i.score}) {"*" if i.was_bingo else ""} (A{i.alg})' for i in self.best_moves[-15:]]]
        for index, i in enumerate(options):
            message = cn.small_font.render(i, True, (20, 80, 20))
            self.display.blit(message, (cn.BOARD_WIDTH - 300, 10 + (index * 10)))

        if self.preview_index:
            move = self.best_moves[self.preview_index]
            length = move.get_length()
            x = cn.START_X + (move.pos[0] * Board.tile_width)
            y = cn.START_Y + (move.pos[1] * Board.tile_width)
            width = Board.tile_width * length if move.dir == constants.HORIZONTAL else Board.tile_width
            height = Board.tile_width * length if move.dir == constants.VERTICAL else Board.tile_width

            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            green = (120, 170, 120, 170)
            surface.fill(green)

            for index, l in enumerate(move.word):
                half = Board.tile_width / 2
                letter = cn.font.render(l.upper(), True, (0, 0, 0))
                textRect = letter.get_rect()
                textRect.center = (half,  Board.tile_width * index + half + 3) if move.dir == constants.VERTICAL else (Board.tile_width * index + half, half + 3)
                surface.blit(letter, textRect)

            self.display.blit(surface, (x, y))


    def get_selected_tile(self):
        if cn.clicked:
            x, y = cn.mouse_pos
            new_x, new_y = ((x - cn.START_X) // Board.tile_width, (y - cn.START_Y) // Board.tile_width)
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
                self.best_moves = algorithms.find_best_move(self.board.values, self.letters)
                self.preview_index = None
            return

        # letter changing
        if self.setting_letters:
            if isinstance(new_value, str):
                self.letters.append(new_value)
            elif self.letters:
                self.letters = self.letters[:-1]
            self.save_board()
            return

        if isinstance(new_value, int):
            if new_value == 0 and self.preview_index:
                move = self.best_moves[self.preview_index]
                board_utils.place_word(self.board.values, move.word, move.pos, move.dir)

                self.preview_index = None
                self.letters = algorithms.subtract_arrays(self.letters, list(move.word))
                self.total_score += move.score

            elif new_value <= len(self.best_moves):
                self.preview_index = -1 * new_value
            return

        if new_value in ['left', 'right']:
            boards = board_cycling.get_boards()
            direction = -1 if new_value == 'left' else 1
            if str(self.board_number + direction) in boards:
                self.board_number += direction
                self.load_board()
            return

        new_value = '' if not new_value else new_value
        self.board.values[y][x] = new_value
        self.save_board()
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




    def add_board(self):
        boards = board_cycling.get_boards()
        new_board_number = int(boards[-1]) + 1 if boards else self.board_number
        empty_board = [['' for x in range(cn.COLUMNS)] for y in range(cn.ROWS)]
        board_cycling.update_board(new_board_number, empty_board, [], 0)
        self.board_number = new_board_number
        self.load_board()

    def delete_board(self):
        boards = board_cycling.get_boards()
        if len(boards) > 1:
            board_cycling.delete_board(self.board_number)
            boards = board_cycling.get_boards()
            self.board_number = int(boards[0])
            self.load_board()

    def load_board(self):
        board_data = board_cycling.load_board(self.board_number)
        self.board.values = board_data['board_values']
        self.letters = board_data['letters']
        self.total_score = board_data['score']

    def save_board(self):
        board_cycling.update_board(self.board_number, self.board.values, self.letters, self.total_score)

