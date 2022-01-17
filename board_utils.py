import numpy as np

import constants as cn
from constants import HORIZONTAL, VERTICAL


def find_all_words(board_values: list):
    horizontal_map = [[0 for i in range(cn.COLUMNS)] for i in range(cn.ROWS)]
    vertical_map = [[0 for i in range(cn.COLUMNS)] for i in range(cn.ROWS)]
    words = []

    for y in range(cn.ROWS):
        for x in range(cn.COLUMNS):
            value = board_values[y][x]
            if not value:  # not blank
                continue
            next_x = x + 1
            next_y = y + 1

            if next_x in range(cn.COLUMNS) and not horizontal_map[y][x] and board_values[y][next_x]:
                row = list(board_values[y][x:])
                width = row.index('') if '' in row else cn.COLUMNS - x
                for i in range(x, x + width):
                    horizontal_map[y][i] = 1
                if width > 1:
                    words.append((''.join(board_values[y][x:x + width]), (x, y), HORIZONTAL))  # x, y

            if next_y in range(cn.ROWS) and not vertical_map[y][x] and board_values[next_y][x]:
                col = [board_values[i][x] for i in range(cn.ROWS)][y:]
                height = col.index('') if '' in col else cn.ROWS - y

                for i in range(y, y + height):
                    vertical_map[i][x] = 1
                if height > 1:
                    words.append(
                        (''.join([board_values[i][x] for i in range(y, y + height)]), (x, y), VERTICAL))  # x, y

    return words


def place_word(board_values, word, pos, direction):
    x, y = pos
    for i in range(len(word)):
        if direction == HORIZONTAL:
            board_values[y][x + i] = word[i]
        elif direction == VERTICAL:
            board_values[y + i][x] = word[i]


def get_valid_words(words):
    return [i for i in words if i[0] in cn.hashed_dictionary]


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


def invalid_board_state(board_values):
    words = find_all_words(board_values)
    valid = get_valid_words(words)
    if len(valid) != len(words):
        return [i for i in words if i not in valid]
    return False


def tiles_connected(board_values):
    visited_nodes = []

    def DFS(neighbors):
        for i in neighbors:
            x, y = i
            if 0 <= i[0] < cn.COLUMNS and 0 <= i[
                1] < cn.ROWS and i not in visited_nodes:  # checks if the neighbor is in the board
                if board_values[y][x]:
                    visited_nodes.append(i)
                    new_neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]  # immediate adjacent neighbors
                    DFS(new_neighbors)

    cX, cY = cn.COLUMNS // 2, cn.ROWS // 2
    DFS(
        [(cX - 1, cY), (cX + 1, cY), (cX, cY - 1), (cX, cY + 1)]
    )

    board_values = np.array(board_values)
    tiles_placed = np.count_nonzero(board_values != '')
    return len(visited_nodes) == tiles_placed


def point_on_screen(pos):
    x, y = pos
    return x in range(cn.COLUMNS) and y in range(cn.ROWS)