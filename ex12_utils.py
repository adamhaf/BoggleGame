#################################################
# FILE : .py
# WRITER : Adam Haftzadi, 315359737, Ori Atary ,ori.ata ,adamhaf
# EXERCISE : intro2cs2 ex12 2021
##################################################
import copy
BOARD_SIZE = 4
SQUARE_ROOT_2 = 2 ** 0.5
ZERO = 0
DIRECTION_DIC = {"right": (0, 1), "down": (1, 0), "up": (-1, 0),
                 "left": (0, -1),
                 "up-left": (-1, -1),
                 "up-right": (-1, 1), "down-left": (1, -1),
                 "down-right": (1, 1)}


def points_distance(point1_x, point1_y, point2_x, point2_y):
    """with the pthgorinage therm we will measure the distance between
    2 dots """
    x_dis = (point1_x - point2_x) ** 2
    y_dis = (point1_y - point2_y) ** 2
    distance = (x_dis + y_dis) ** 0.5
    if distance == 1 or distance == SQUARE_ROOT_2:
        return True
    return False


def is_valid_path(board, path, words):
    """here we will go over the board,
    we will build the word according to the path that we got."""
    if not path:
        return None
    word = ""
    last_point = [path[0][0] + 1, path[0][1]]  # just and arbitrary distance
    for str_path in path:

        # checking if there is duplication
        if path.count(str_path) >= 2:
            return None

        if not points_distance(last_point[0], last_point[1], str_path[0],
                               str_path[1]):
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


def find_length_n_paths(n, board, words):
    """here we will send the appropriate parameter
    to length_or_path function """
    if n > BOARD_SIZE ** 2:
        return []
    return length_or_paths(n, board, words, False)


def length_or_paths(n, board, words, words_len_search):
    """this function is a shall to find_length_word_or_path:
    we will send every cell in the matrix to function find_length_word_or_path
    we will take only words that is in the right length
    """
    paths_list = []
    path = []
    # taking only the words that can be fit
    if words_len_search:
        updated_word_list = [word for word in words if len(word) == n]
    else:
        updated_word_list = [word for word in words if len(word) >= n]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            location = i, j
            path.append(location)
            find_length_word_or_path(updated_word_list, board, DIRECTION_DIC,
                                     path, paths_list, n, words_len_search)
            path = []  # zeroing path

    return paths_list


def longest_length_possible_word(board):
    """here we will check what is the longest word that we can build,
    and by that we will know wthere we need to get to the recursion"""
    str_list = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            str_list.append(board[row][col])
    word_joined_str = ''.join(str_list)
    return len(word_joined_str)


def find_length_n_words(n, board, words):
    """here we will send appropriate parameters to length_or_paths for
    searching by word length"""
    if n > longest_length_possible_word(board):
        return []
    return length_or_paths(n, board, words, True)


def coordinate_is_valid(coordinate):
    """making sure the the coordinate is vaild"""
    if coordinate:
        if coordinate[0] < BOARD_SIZE and coordinate[1] < BOARD_SIZE:
            return True
        else:
            return False


def current_path_word(board, path):
    """building a word from path on a board"""
    str_list = []
    current_word = None
    for coordinate in path:
        if coordinate and coordinate_is_valid(coordinate):
            str_list.append(board[coordinate[0]][coordinate[1]])
            current_word = ''.join(str_list)
    return current_word


def check_if_word_slice_relevant(path_word, words):
    """checking if the slice is a part of a word from the words"""
    flag = False
    for word in words:
        if word[0:len(path_word)] == path_word:
            flag = True
            break
    return flag


def words_filter(words, current_word_from_path):
    new_list = []
    for word in words:
        str_len = len(current_word_from_path)
        if word[0:str_len] == current_word_from_path:
            new_list.append(word)
    return new_list


def find_length_word_or_path(words, board, direction_dict, path, paths_list,
                             n, words_len_search):
    """in this recursive function we will do the following:
    1) exit rules will be depends on words_len_search:
        words_len_search is True
        so that mean we are searching for word length
        words_len_search is False
        so we are making sure that we have an appropriate length path
    2)
        we will go recursive on every direction
        we will make sure before entering to recursive call that we arent out
        of the board.

    """
    if len(path) > n:
        return

    current_word_from_path = current_path_word(board, path)
    if not check_if_word_slice_relevant(current_word_from_path, words):
        return

    if words_len_search and len(current_word_from_path) == n:
        correct_word = is_valid_path(board, path, words)
        if correct_word and path not in paths_list:
            paths_list.append(path[:])
            return

    elif not words_len_search and len(path) == n:
        correct_word = is_valid_path(board, path, words)
        if correct_word and path not in paths_list:
            paths_list.append(path[:])
            return

    for direction in DIRECTION_DIC.values():

        next_location = path[-1][0] + direction[0], path[-1][1] + direction[1]
        if next_location[0] < 0 or next_location[1] < 0 or next_location[
            0] > BOARD_SIZE - 1 or next_location[1] > BOARD_SIZE - 1:
            continue
        if next_location not in path:
            new_path = copy.deepcopy(path)
            new_path.append(next_location)
            current_word_from_path = current_path_word(board, path)
            words_filtered = words_filter(words, current_word_from_path)
            find_length_word_or_path(words_filtered, board, direction_dict,
                                     new_path,
                                     paths_list, n, words_len_search)

def max_score_paths(board, words):
    """we will go over all length path starting on the square of the size
    of the board.
    by starting from the longest path we know that we will get the word longest
    path, so we are maximizing the path for each word."""
    path_list = []
    word_list = []
    for i in range(BOARD_SIZE ** 2, 0, -1):
        temp_path = find_length_n_paths(i, board, words)
        if temp_path:
            for path in temp_path:
                word_from_path = current_path_word(board, path)
                if word_from_path not in word_list:
                    path_list.append(path)
                    word_list.append(word_from_path)
    return path_list


def list_from_words_file(file_name):
    """simple loading text file"""
    list_of_words = []
    with open(file_name) as file:
        for line in file:
            list_of_words.append(line.rstrip())
    return list_of_words


