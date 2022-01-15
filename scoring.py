import numpy as np

import constants as cn
from word import find_all_words, get_valid_words, HORIZONTAL, VERTICAL


def calculate_entire_board_score(board_values):
    words = find_all_words(board_values)
    valid = get_valid_words(words)
    return sum(score_word(board_values, i) for i in valid)  # returns the sum of all word scores


def calculate_move_score(board_values, case_values, letters):
    current_board_score = calculate_entire_board_score(board_values)
    case_board_score = calculate_entire_board_score(case_values)
    score = case_board_score - current_board_score

    # adds 50 points if you use all letters in your hand
    bingo = False
    board_values = np.array(board_values)
    case_values = np.array(case_values)
    tiles_placed_board = np.count_nonzero(board_values != '')
    tiles_placed_case = np.count_nonzero(case_values != '')
    if tiles_placed_case - tiles_placed_board == len(letters):
        score += 50
        bingo = True

    return score, bingo


def calculate_score(board_values, word, tiles):
    points = [cn.LETTER_POINTS[letter] for letter in word]

    for index, letter in enumerate(word):
        x, y = tiles[index]
        multiplier = cn.multipliers[y][x]
        if multiplier == cn.DOUBLE_LETTER_SCORE and not board_values[y][x]:
            points[index] *= 2
        if multiplier == cn.TRIPLE_LETTER_SCORE and not board_values[y][x]:
            points[index] *= 3
        if multiplier == cn.DOUBLE_WORD_SCORE and not board_values[y][x]:
            points = np.array(points)
            points *= 2
            points = list(points)
        if multiplier == cn.TRIPLE_WORD_SCORE and not board_values[y][x]:
            points = np.array(points)
            points *= 3
            points = list(points)

    return sum(points)


def score_word(board_values, info):
    word, starting_pos, direction = info
    x, y = starting_pos

    if direction == HORIZONTAL:
        tiles = [(i, y) for i in range(x, x + len(word))]  # x, y
        return calculate_score(board_values, word, tiles)
        # print(word, calculate_score(word, tiles))

    if direction == VERTICAL:
        tiles = [(x, i) for i in range(y, y + len(word))]  # x, y
        return calculate_score(board_values, word, tiles)
        # print(word, calculate_score(word, tiles))