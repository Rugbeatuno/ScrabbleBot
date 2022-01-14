import multiprocessing

import time
import numpy as np
import re

import constants as cn
from solver import get_combos

with open('scrabble_words.txt', 'r') as file:
    dictionary = file.readlines()
    dictionary = [i.replace('\n', '') for i in dictionary]
    hashed_dictionary = {i: 0 for i in dictionary}

HORIZONTAL = 0
VERTICAL = 1

manager = multiprocessing.Manager()
possible_moves = manager.list()


def find_all_words(board_values):
    horizontal_map = [[0 for i in range(cn.COLUMNS)] for i in range(cn.ROWS)]
    vertical_map = [[0 for i in range(cn.COLUMNS)] for i in range(cn.ROWS)]
    words = []
    for j in range(cn.ROWS):
        for i in range(cn.COLUMNS):
            value = board_values[j][i]
            if value:  # not blank
                # we will check for horizontal words first
                # continue to move right until we hit the edge of the board or the end of the word
                # however, to prevent repeating over the same segment of a word
                # we will store the locations of already seen words and just skip over them
                width = 0
                while True:
                    next_pos = i + width
                    if next_pos < cn.COLUMNS and board_values[j][next_pos]:
                        if horizontal_map[j][next_pos]:
                            break
                        width += 1
                        horizontal_map[j][i + width - 1] = 1
                    else:
                        if width > 1:
                            stuff = board_values[j][i:i + width]
                            text = ''.join(stuff)
                            words.append((text, (i, j), HORIZONTAL))  # x, y
                        break

                # now vertically
                height = 0
                while True:
                    next_pos = j + height
                    if next_pos < cn.ROWS and board_values[next_pos][i]:
                        if vertical_map[next_pos][i]:
                            break
                        height += 1
                        vertical_map[j + height - 1][i] = 1
                    else:
                        if height > 1:
                            stuff = [board_values[y][i] for y in range(j, j + height)]
                            text = ''.join(stuff)
                            words.append((text, (i, j), VERTICAL))  # x, y
                        break
    return words


def tiles_connected(board_values):
    visited_nodes = []
    def DFS(neighbors):
        for i in neighbors:
            x, y = i
            if 0 <= i[0] < cn.COLUMNS and 0 <= i[1] < cn.ROWS and i not in visited_nodes:  # checks if the neighbor is in the board
                if board_values[y][x]:
                    visited_nodes.append(i)
                    new_neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]  # immediate adjacent neighbors
                    DFS(new_neighbors)

    cX, cY = cn.COLUMNS // 2, cn.ROWS // 2
    DFS(
        [(cX - 1, cY), (cX + 1, cY), (cX, cY - 1), (cX, cY + 1)]
    )

    board_values = np.array(board_values)
    tiles_placed = np.count_nonzero(board_values != '')
    return len(visited_nodes) == tiles_placed


def invalid_board_state(board_values):
    words = find_all_words(board_values)
    valid = get_valid_words(words)
    if len(valid) != len(words):
        return [i for i in words if i not in valid]
    return False


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


def get_valid_words(words):
    return [i for i in words if i[0] in hashed_dictionary]


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


def place_word(board_values, word, pos, direction):
    x, y = pos
    for i in range(len(word)):
        if direction == HORIZONTAL:
            board_values[y][x + i] = word[i]
        elif direction == VERTICAL:
            board_values[y + i][x] = word[i]


def valid_word_placement(board_values, word, pos, direction):
    try:
        x, y = pos
        length = len(word)

        if direction == HORIZONTAL and x + length - 1 < cn.COLUMNS:
            desired_area = board_values[y][x:x + length]
        elif direction == VERTICAL and y + length - 1 < cn.ROWS:
            desired_area = [board_values[y + i][x] for i in range(length)]
        else:
            return False

        for i in range(len(desired_area)):
            value = board_values[y + i][x] if direction == VERTICAL else board_values[y][x + i]
            if value and value != word[i]:  # if a letter is preventing this word then break
                return False

        case = list(np.array(board_values).copy())
        place_word(case, word, (x, y), direction)

        if not invalid_board_state(case):
            return case
    except IndexError:
        pass



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


def subtract_arrays(arr1, arr2):
    for i in arr2:
        if i in arr1:
            arr1.remove(i)
    return arr1


def log_if_word_valid(current_board_values, word, starting_pos, direction, letters, algorithm, do_connectivity_check=False):
    case = valid_word_placement(current_board_values, word, starting_pos, direction)

    if case:
        if do_connectivity_check and not tiles_connected(case):
            return

        score, was_bingo = calculate_move_score(current_board_values, case, letters)
        if score > 0:
            data = {
                'word': word,
                'start_pos': starting_pos,
                'dir': direction,
                'score': score,
                'bingo': was_bingo,
                'algorithm': algorithm
            }
            possible_moves.append(data)  # x, y


def find_best_move(board_values, letters):
    global possible_moves
    possible_moves = manager.list()  # special way of clearing ListProxy
    s = time.time()

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
    # algorithm_part_1(board_values, letters)
    print(f'alg 1 : {time.time()-s}')
    # s = time.time()
    # algorithm_part_2(board_values, letters)
    # print(f'alg 2 : {time.time() - s}')
    # s = time.time()
    # algorithm_part_3(board_values, letters)
    # print(f'alg 3 : {time.time() - s}')
    # s = time.time()
    # algorithm_part_4(board_values, letters)
    # print(f'alg 4 : {time.time() - s}')

    possible_moves = sorted(possible_moves, key=lambda i: i['score'])
    return possible_moves


def algorithm_part_1(board_values, letters):
    for y in range(cn.ROWS):
        for x in range(cn.COLUMNS):
            letter = board_values[y][x]
            if not letter:
                continue

            check_directions = []
            try:
                if not board_values[y-1][x] and not board_values[y+1][x]:  # if tiles above and below are both empty
                    check_directions.append(VERTICAL)
            except IndexError:
                pass
            try:
                if not board_values[y][x-1] and not board_values[y][x+1]:  # if tiles to the left and right are both empty
                    check_directions.append(HORIZONTAL)
            except IndexError:
                pass

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
                        log_if_word_valid(board_values, word, (start_pos, y), HORIZONTAL, letters, 1)

                    if VERTICAL in check_directions:
                        start_pos = y - index
                        log_if_word_valid(board_values, word, (x, start_pos), VERTICAL, letters, 1)

    return possible_moves


# word extending algorithm
def algorithm_part_2(board_values, letters):
    words = find_all_words(board_values)

    for i in words:
        possible_matches = []
        word, pos, direction = i
        x, y = pos

        possible_matches.extend([j for j in dictionary if word in j])
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


# word end slider algorithm
def algorithm_part_3(board_values, letters):
    words = find_all_words(board_values)
    combos = get_combos(letters)

    for w in words:
        word, pos, direction = w
        x, y = pos
        tile_positions = []

        for combo in combos:
            combo_word, length = combo
            length = len(word)
            combo_word_length = len(combo_word)
            if direction == HORIZONTAL and 0 < x < cn.COLUMNS - 1 and y < cn.ROWS - 1:
                tile_positions = [(x - 1, i, VERTICAL) for i in range(y - combo_word_length + 1, y + 1)]  # x, y, direction (perpendicular)
                tile_positions.extend([(x + length, i, VERTICAL) for i in range(y - combo_word_length + 1, y + 1)])
            if direction == VERTICAL and 0 < y < cn.ROWS - 1 and x < cn.COLUMNS - 1:
                tile_positions = [(i, y - 1, HORIZONTAL) for i in range(x - combo_word_length + 1, x + 1)]  # x, y, direction (perpendicular)
                tile_positions.extend([(i, y + length, HORIZONTAL) for i in range(x - combo_word_length + 1, x + 1)])
            for tile in tile_positions:
                tile_pos, tile_direction = tile[:2], tile[-1]
                log_if_word_valid(board_values, combo_word, tile_pos, tile_direction, letters, 3)


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