#################################################
# FILE : .py
# WRITER : Adam Haftzadi, 315359737, Ori Atary ,ori.ata ,adamhaf
# EXERCISE : intro2cs2 ex12 2021
##################################################
import boggle_board_randomizer
from copy import deepcopy

BOARD_SIZE = 4
SQUARE_ROOT_2 = 2 ** 0.5
ZERO = 0
DIRECTION_DIC = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1), "up-left": (-1, -1),
                 "up-right": (-1, 1), "down-left": (1, -1), "down-right": (1, 1)}


def points_distance(point1_x, point1_y, point2_x, point2_y):
    x_dis = (point1_x - point2_x) ** 2
    y_dis = (point1_y - point2_y) ** 2
    distance = (x_dis + y_dis) ** 0.5
    if distance == 1 or distance == SQUARE_ROOT_2:
        return True
    return False


def is_valid_path(board, path, words):
    """here we will go over the board, we will build the word according to the path that we got."""
    word = ""
    last_point = [path[0][0] + 1, path[0][1]]  # just and arbitrary distance
    for str_path in path:

        # checking if there is duplication
        if path.count(str_path) >= 2:
            return None

        if not points_distance(last_point[0], last_point[1], str_path[0], str_path[1]):
            return None
        if str_path[0] < 0 or str_path[1] < 0:
            return None
        if str_path[0] < BOARD_SIZE and str_path[1] < BOARD_SIZE:
            word += board[str_path[0]][str_path[1]]
        else:
            return None
        last_point = [str_path[0], str_path[1]]

    if word in words:
        return word


def efficient_dict(location, current_path):
    efficient_dic = deepcopy(DIRECTION_DIC)
    try:
        if location[0] <= ZERO:
            del efficient_dic["up"]
            del efficient_dic["up-left"]
            del efficient_dic["up-right"]
        if location[0] >= BOARD_SIZE - 1:
            del efficient_dic["down"]
            del efficient_dic["down-left"]
            del efficient_dic["down-right"]
        if location[1] <= ZERO:
            del efficient_dic["left"]
            del efficient_dic["down-left"]
            del efficient_dic["up-left"]
        if location[1] >= BOARD_SIZE - 1:
            del efficient_dic["right"]
            del efficient_dic["down-right"]
            del efficient_dic["up-right"]

        # after we cleared all the ilegal directions determined only by location on board
        # we want to clear the ileagal directions determined by the current route

    except KeyError:  # relax dude
        pass

    list_of_survived_keys = [key for key in efficient_dic.keys()]
    for key in list_of_survived_keys:
        new_location = location[0] + efficient_dic[key][0], location[1] + efficient_dic[key][1]
        if new_location in current_path:
            del efficient_dic[key]

    return efficient_dic


def find_length_n_paths(n, board, words):
    paths_list = []
    path = []
    updated_word_list = [word for word in words if len(word) >= n]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            location = i, j
            path.append(location)
            find_length_n_paths_helper(updated_word_list, board, DIRECTION_DIC, path, paths_list, n)
            path = []  # zeroing path

    if paths_list:
        return paths_list


def check_if_word_slice_relevant(path_word, words):
    flag = False
    for word in words:
        if word[0:len(path_word)] == path_word:
            flag = True
            break
    return flag


def coordinate_is_valid(coordinate):
    if coordinate:
        if coordinate[0] < BOARD_SIZE and coordinate[1] < BOARD_SIZE:
            return True
        else:
            return False


def current_path_word(board, path):
    str_list = []
    current_word = None
    for coordinate in path:
        if coordinate and coordinate_is_valid(coordinate):
            str_list.append(board[coordinate[0]][coordinate[1]])
            current_word = ''.join(str_list)
    return current_word


def find_length_n_paths_helper(words, board, direction_dict, path, paths_list, n):
    if len(path) == n:
        if is_valid_path(board, path, words) and path not in paths_list:
            paths_list.append(path)
        return

    current_word_from_path = current_path_word(board, path)
    if not check_if_word_slice_relevant(current_word_from_path, words):
        return

    current_location = path[-1][0], path[-1][1]
    legit_direction_dict = efficient_dict(current_location, path)
    for direction in legit_direction_dict.values():
        next_location = path[-1][0] + direction[0], path[-1][1] + direction[1]
        if next_location not in path:
            updated_path = deepcopy(path)
            updated_path.append(next_location)
            find_length_n_paths_helper(words, board, direction_dict, updated_path, paths_list, n)


def find_length_n_words(n, board, words):
    paths_list = []
    path = []
    updated_word_list = [word for word in words if len(word) == n]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            location = i, j
            path.append(location)
            find_length_n_words_helper(updated_word_list, board, DIRECTION_DIC, path, paths_list, n)
            path = []  # zeroing path

    if paths_list:
        return paths_list


def find_length_n_words_helper(words, board, direction_dict, path, paths_list, n):
    if is_valid_path(board, path, words) and len(is_valid_path(board, path, words)) == n and path not in paths_list:
        paths_list.append(path)
        return
    if len(path) > n:
        return

    current_location = path[-1][0], path[-1][1]
    legit_direction_dict = efficient_dict(current_location)

    for direction in legit_direction_dict.values():
        next_location = path[-1][0] + direction[0], path[-1][1] + direction[1]
        if next_location not in path:
            updated_path = deepcopy(path)
            updated_path.append(next_location)
            find_length_n_words_helper(words, board, direction_dict, updated_path, paths_list, n)


def max_score_paths(board, words):
    path_list = []
    word_list = []
    for i in range(BOARD_SIZE ** 2, 0, -1):
        temp_path = find_length_n_paths(i, board, words)
        print("finished iteration on: ", i)
        if temp_path:
            for path in temp_path:
                path_word = is_valid_path(board, path, words)
                if path_word not in word_list:
                    path_list.append(path)
                    word_list.append(path_word)
    return path_list


def list_from_words_file(file_name):
    list_of_words = []
    with open(file_name) as file:
        for line in file:
            list_of_words.append(line.rstrip())
    return list_of_words


from pprint import pprint

board1 = [["a", "bxx", "askjdhasjdhjkasdhjasdjkashdc", "d"],
          ["e", "f", "gx", "g"],
          ["h", "iz", "g", "k"],
          ["l", "m", "n", "o"]]

board2 = [['L', 'E', 'O', 'F'],
          ['E', 'P', 'I', 'E'],
          ['R', 'T', 'L', 'D'],
          ['N', 'B', 'Y', 'H']]
words = ["bxxgxg", "bxxgxiz", "bxxgxgn", "abdd", "cgg", "aehlmnok", "dg", "dc",
         "abxxaskjdhsjdhjkasdhjasdjkashdcdggxfehizgkonml"]

word_list = list_from_words_file("boggle_dict.txt")
board = boggle_board_randomizer.randomize_board()
pprint(board2)

max_score_paths(board, word_list)
