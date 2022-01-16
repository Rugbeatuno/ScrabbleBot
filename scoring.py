import numpy as np

import constants as cn
from board_utils import find_all_words, get_valid_words, place_word, invalid_board_state


def check_for_bingo(board_values, case_values, letters):
    board_values = np.array(board_values)
    case_values = np.array(case_values)
    tiles_placed_board = np.count_nonzero(board_values != '')
    tiles_placed_case = np.count_nonzero(case_values != '')
    return tiles_placed_case - tiles_placed_board == len(letters)


def calculate_move_score(board_values, word, letters):
    score = 0
    bingo = False  # adds 50 points if you use all letters in your hand

    original_words = find_all_words(board_values)
    original_words = get_valid_words(original_words)

    board_values = np.array(board_values)
    case_values = board_values.copy()
    board_values = list(board_values)
    place_word(case_values, word['word'], word['start_pos'], word['dir'])
    words = find_all_words(case_values)
    valid = get_valid_words(words)

    for i in valid:
        if i in original_words:
            continue
        board_values = np.array(board_values)
        case_values = board_values.copy()
        board_values = list(board_values)
        place_word(case_values, i[0], i[1], i[2])
        if invalid_board_state(case_values):
            continue

        x, y = i[1]
        tiles = [(i, y) for i in range(x, x + len(i[0]))] if i[2] == cn.HORIZONTAL else [(x, i) for i in
                                                                                         range(y, y + len(i[0]))]
        score += calculate_score(board_values, i[0], tiles)

    if check_for_bingo(board_values, case_values, letters):
        score += 50
        bingo = True
    return score, bingo


def calculate_score(board_values, word, tiles):
    points = [cn.LETTER_POINTS[letter] for letter in word]
    points = np.array(points)

    for index, letter in enumerate(word):
        x, y = tiles[index]
        multiplier = cn.multipliers[y][x]
        if multiplier == cn.DOUBLE_LETTER_SCORE and not board_values[y][x]:
            points[index] *= 2
        if multiplier == cn.TRIPLE_LETTER_SCORE and not board_values[y][x]:
            points[index] *= 3
        if multiplier == cn.DOUBLE_WORD_SCORE and not board_values[y][x]:
            points *= 2
        if multiplier == cn.TRIPLE_WORD_SCORE and not board_values[y][x]:
            points *= 3

    return sum(list(points))
