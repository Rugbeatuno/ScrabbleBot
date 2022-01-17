import multiprocessing

import time
import re

import constants as cn

from word import Word
from board_utils import find_all_words, valid_word_placement, tiles_connected, point_on_screen
from constants import HORIZONTAL, VERTICAL
from solver import get_combos
from scoring import calculate_move_score

manager = multiprocessing.Manager()
possible_moves = manager.list()

# there will be 2 approaches in this algorithm
# the first will start off by iterating through all tiles on the board
# then compute all words that can be made with those 7+1(8) letters
# finally check if any orientation of those words are valid
# this method will only make words with a length of 8 at max

# the second approach will start off by looking through all horizontal words
# then will attempt to make even longer words up to the length of 15
# this method is unfinished

'''
Example:

     a
     v
   t o m a t o
     c
     a
     d
     o
'''


def subtract_arrays(arr1: list, arr2: list) -> list:
    for i in arr2:
        if i in arr1:
            arr1.remove(i)
    return arr1


def log_if_word_valid(current_board_values, word, starting_pos, direction, letters, algorithm,
                      do_connectivity_check=False):
    case = valid_word_placement(current_board_values, word, starting_pos, direction)

    if case:
        if do_connectivity_check and not tiles_connected(case):
            return

        score, was_bingo = calculate_move_score(
            current_board_values,
            {'word': word, 'start_pos': starting_pos, 'dir': direction},
            letters
        )
        if score:
            data = Word(word, starting_pos, direction, score, was_bingo, algorithm)
            possible_moves.append(data)  # x, y


def find_best_move(board_values: list, letters: list) -> list:
    global possible_moves
    possible_moves = manager.list()  # special way of clearing ListProxy
    s = time.perf_counter()

    a1 = multiprocessing.Process(target=algorithm_part_1, args=(board_values, letters))
    a2 = multiprocessing.Process(target=algorithm_part_2, args=(board_values, letters))
    a3 = multiprocessing.Process(target=algorithm_part_3, args=(board_values, letters))
    a4 = multiprocessing.Process(target=algorithm_part_4, args=(board_values, letters))
    a1.start()
    a2.start()
    a3.start()
    a4.start()
    a1.join()
    a2.join()
    a3.join()
    a4.join()

    print(f'algs : {time.perf_counter() - s}')

    return sorted(possible_moves, key=lambda i: i.score)


def algorithm_part_1(board_values, letters):
    for y in range(cn.ROWS):
        for x in range(cn.COLUMNS):
            letter = board_values[y][x]
            if not letter:
                continue

            check_directions = [VERTICAL, HORIZONTAL]
            if point_on_screen((x, y - 1)) and board_values[y - 1][x]:  # if tiles above and below are both empty
                check_directions.remove(VERTICAL)
            elif point_on_screen((x, y + 1)) and board_values[y + 1][x]:
                check_directions.remove(VERTICAL)
            if point_on_screen((x + 1, y)) and board_values[y][x + 1]:  # if tiles above and below are both empty
                check_directions.remove(HORIZONTAL)
            elif point_on_screen((x - 1, y)) and board_values[y][x - 1]:
                check_directions.remove(HORIZONTAL)

            if not check_directions:
                continue

            letters_copy = letters.copy()
            letters_copy.append(letter)
            combos = get_combos(letters_copy)
            combos = [i for i in combos if letter in i[0]]
            for i in combos:
                word, length = i
                letter_indexes = [i.start() for i in re.finditer(letter, word)]

                # horizontal checks first then vertically
                for index in letter_indexes:
                    if HORIZONTAL in check_directions:
                        start_pos = x - index
                        if point_on_screen((start_pos, y)):
                            log_if_word_valid(board_values, word, (start_pos, y), HORIZONTAL, letters, 1)

                    if VERTICAL in check_directions:
                        start_pos = y - index
                        if point_on_screen((x, start_pos)):
                            log_if_word_valid(board_values, word, (x, start_pos), VERTICAL, letters, 1)

    return possible_moves


# word extending algorithm
def algorithm_part_2(board_values, letters):
    words = find_all_words(board_values)

    for i in words:
        possible_matches = []
        word, pos, direction = i
        x, y = pos

        possible_matches.extend([j for j in cn.dictionary if word in j])
        for match in possible_matches:
            offset = 0 - match.index(word)
            starting_pos = (x + offset, y) if direction == HORIZONTAL else (x, y + offset)
            unneeded_letters = []

            if starting_pos[0] < 0 or starting_pos[1] < 0:
                continue
            required_letters = subtract_arrays(list(match), unneeded_letters)
            required_letters = subtract_arrays(required_letters, list(word))
            if not subtract_arrays(required_letters, letters):  # if the word can be made
                log_if_word_valid(board_values, match, starting_pos, direction, letters, 2)


# word slider algorithm
def algorithm_part_3(board_values, letters):
    anchor_nodes = []
    adjacent_pos = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for y in range(cn.ROWS):
        for x in range(cn.COLUMNS):
            value = board_values[y][x]
            if not value:
                continue

            for delta_x, delta_y in adjacent_pos:
                new_pos = (x + delta_x, y + delta_y)
                if point_on_screen(new_pos) and not board_values[new_pos[1]][new_pos[0]] and new_pos not in anchor_nodes:
                    anchor_nodes.append(new_pos)

    for word in get_combos(letters):
        for anchor in anchor_nodes:
            x, y = anchor
            tile_checks = []

            for i in range(1, len(word[0])):
                new_pos_h = (x - i, y)
                new_pos_v = (x, y - i)
                if point_on_screen(new_pos_h):
                    tile_checks.append((new_pos_h, HORIZONTAL))
                if point_on_screen(new_pos_v):
                    tile_checks.append((new_pos_v, VERTICAL))

            tile_checks = list(set(tile_checks))
            for tile_pos, tile_direction in tile_checks:
                log_if_word_valid(board_values, word[0], tile_pos, tile_direction, letters, 3)


# words inbetween check
def algorithm_part_4(board_values, letters):
    words = find_all_words(board_values)

    for y in range(cn.ROWS):
        row = [i for i in board_values[y] if i]

        for i in words:
            if i[1][1] == y and i[2] == HORIZONTAL:
                for j in i[0]:
                    if j in row:
                        row.remove(j)

        if len(row) <= 1:
            continue
        row.extend(letters)
        row_combos = get_combos(''.join(row))
        for x in range(cn.COLUMNS):
            for i in row_combos:
                if i[1] > 3:
                    try:
                        tiles = board_values[y][x:x + i[1]]
                        tiles.extend(letters)
                        if not subtract_arrays(list(i[0]), tiles):
                            log_if_word_valid(board_values, i[0], (x, y), HORIZONTAL, letters, 4, True)
                    except IndexError:
                        continue

    for x in range(cn.COLUMNS):
        column = [board_values[i][x] for i in range(cn.ROWS) if board_values[i][x]]
        # if not column:
        #     continue
        for i in words:
            if i[1][0] == x and i[2] == VERTICAL:
                for j in i[0]:
                    if j in column:
                        column.remove(j)
        if len(column) <= 1:
            continue
        column.extend(letters)
        row_combos = get_combos(''.join(column))
        for y in range(cn.ROWS):
            for i in row_combos:
                if i[1] > 3:
                    try:
                        tiles = [board_values[i][x] for i in range(y, y + i[1])]
                        tiles.extend(letters)
                        if not subtract_arrays(list(i[0]), tiles):
                            log_if_word_valid(board_values, i[0], (x, y), VERTICAL, letters, 4, True)
                    except IndexError:
                        pass
