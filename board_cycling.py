import json
filename = 'boards.json'


def update_board(board_number, board_values, letters, score):
    board_number = str(board_number)

    with open(filename, 'r') as f:
        data = json.load(f)
        if board_number not in data:
            data[board_number] = {}
        data[board_number]['board_values'] = board_values
        data[board_number]['letters'] = letters
        data[board_number]['score'] = score

    with open(filename, 'w') as f:
        json.dump(data, f, sort_keys=True)


def load_board(board_number):
    with open(filename, 'r') as f:
        data = json.load(f)
        return data[str(board_number)]


def get_boards():
    with open(filename, 'r') as f:
        data = json.load(f)
        return list(data.keys())


def delete_board(board_number):
    board_number = str(board_number)
    new_dict = {}
    with open(filename, 'r') as f:
        data = json.load(f)
        del data[board_number]

        for i in list(data.keys()):
            if int(i) > int(board_number):
                new_dict[int(i)-1] = data.pop(i)
            else:
                new_dict[i] = data.pop(i)

    with open(filename, 'w') as f:
        json.dump(new_dict, f, sort_keys=True)