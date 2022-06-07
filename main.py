import boggle_board_randomizer
import tkinter as tk
import ex12_utils
import time

BORD_SIZE = 4
BUTTON_SIZE_X = 40
BUTTON_SIZE_Y = 20
WIDTH_ENTRY = 35
BORDER_WIDTH_ENTRY = 5
INPUT_GRID_ROW = 50
INPUT_GRID_COL = 10
COL_SPAN = 10
INPUT_X = 100
INPUT_Y = 100
ROW_ADDER = 20
COL_ADDER = 20


class Ui:

    def __init__(self, root, words_path):
        self.board_list = boggle_board_randomizer.randomize_board()
        self.words_list = ex12_utils.list_from_words_file(words_path)
        self.score = 0
        self.timer = 0
        self.main_board = []
        self.button_pressed = []
        self.words_found_list = []
        self.gui_manager(root)

    def get_letters(self):
        letter_list = []
        for i in range(len(self.board_list)):
            for j in range(len(self.board_list[i])):
                self.board_list[i][j]
                letter_list.append()
        return letter_list

    def send_manager(self, player_input):
        pass

    def labels(self):
        def timer():
            minute = time.strftime("%M")
            second = time.strftime("%S")
            label_time.config(text=minute + ": " + second)

        space_label = tk.Label(root, text="")
        label_score = tk.Label(root, text="SCORE : ")
        entry_score = tk.Label(root, text=self.score, width=25, borderwidth=5, bg=None)

        label_timer_title = tk.Label(root, text="TIME : ")
        label_time = tk.Label(root, text="", )
        timer()
        label_words_found = tk.Label(root, text=" Words Found : ")

        space_label.grid(row=27, column=12)
        space_label.grid(row=29, column=12)

        label_score.grid(row=18, column=11, columnspan=2)
        entry_score.grid(row=18, column=13, columnspan=2)
        label_timer_title.grid(row=17, column=11, columnspan=2)
        label_time.grid(row=17, column=13, columnspan=2)
        label_words_found.grid(row=28, column=12, columnspan=2)

    def gui_manager(self, root):
        self.labels()
        self.button_maker(root)

    def button_maker(self, root):
        button_list = []
        letter_list = self.get_letters()
        player_input = tk.Entry(root, width=55, borderwidth=5)
        player_input.grid(row=25, column=11, columnspan=4)
        button_send = tk.Button(root, text="SEND", command=lambda var=player_input: self.user_pressed_send(var))
        button_send.grid(row=26, column=12, columnspan=2)
        for i in range(len(letter_list)):
            button = tk.Button(root, text=letter_list[i], command=lambda i=i:
            self.button_press_main_board_manager(i, player_input),
                               bg='purple', padx=BUTTON_SIZE_X, pady=BUTTON_SIZE_Y)
            button_list.append(button)

        row_adder = ROW_ADDER
        col_adder = COL_ADDER
        for row in range(len(button_list)):
            if row % 4 == 0:
                row_adder += 1
                col_adder = COL_ADDER - 10
            col_adder += 1
            button_list[row].grid(row=row_adder, column=col_adder)
        self.board_list = button_list

    def user_pressed_send(self, player_input):
        word_now = player_input.get()
        if word_now in self.words_found_list:
            print("That word is alredy in founded words list - but in gui msg adammmm")
        elif word_now in self.words_list:
            print('imhere')
            score_to_add = len(word_now) ** 2
            self.score += score_to_add
            self.words_found_list.append(word_now)
            player_input.delete(0, tk.END)
        self.gui_manager(root)

    def button_matrix(self, main_board):
        matrix_main_board = []
        temp_board = []
        counter = 0
        if main_board:
            for i in range(len(main_board)):
                temp_board.append(main_board[i])
                if (i + 1) % BORD_SIZE == 0:
                    matrix_main_board.append(temp_board)
                    temp_board = []
                    counter = 0
                counter += 1
        return matrix_main_board

    def button_press_main_board_manager(self, letter_index, player_input):
        letter_list = self.get_letters()
        current = player_input.get()
        player_input.delete(0, tk.END)
        player_input.insert(0, str(current) + str(letter_list[letter_index]))
        button_matrix = self.button_matrix(self.main_board)
        pressed_poss = (letter_index // BORD_SIZE, letter_index % BORD_SIZE)
        self.button_pressed.append(pressed_poss)

        for i in range(len(button_matrix)):
            for j in range(len(button_matrix[i])):
                if not ex12_utils.points_distance(pressed_poss[0], pressed_poss[1], i, j) or \
                        (i, j) in self.button_pressed:
                    button_matrix[i][j]["state"] = "disabled"
                else:
                    button_matrix[i][j]["state"] = "active"


if __name__ == '__main__':
    # creating the main window'
    root = tk.Tk()
    s = Ui(root, "boggle_dict.txt")
    root.mainloop()
