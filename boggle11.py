from tkinter import messagebox
import boggle_board_randomizer
import tkinter as tk
import ex12_utils

# count down arg
CD_ROW = 17
CD_COL = 11
CD_SPAN = 2
CD_COl_GIRD = 13

# lable

# Game:
BORD_SIZE = 4
GAME_TIME = 180

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
MILISECOND = 1000

# msg
BEGGINING_MSG = "Hey there, would you like to play a game?"
BEGGINING_TITLE = "Welcome menu"
END_OF_TIME_TITLE = "Time Over"
END_OF_TIME_MSG = "Time is over"

RESET_BUTTON = "Reset"

board1 = [["AAH", "AAHED", "AAHING", "AAHS"],
          ["AALS", "AARDVARK", "AARDVARKS", "AARDWOLF"],
          ["h", "iz", "g", "k"],
          ["l", "m", "n", "o"]]

#boggle_board_randomizer.randomize_board()
class Ui:

    def __init__(self, root, words_path):
        self.board_list = board1
        self.words_list = ex12_utils.list_from_words_file(words_path)
        self.score = 0
        self.timer = GAME_TIME
        self.main_board = []
        self.root = root
        self.button_pressed = []
        self.words_found_list = []
        self.gui_manager()
        self.countdown(self.timer)

    def get_letters(self):
        letter_list = []
        for i in range(len(self.board_list)):
            for j in range(len(self.board_list[i])):
                letter_list.append(self.board_list[i][j])
        return letter_list

    def countdown(self, timer):
        label_timer_title = tk.Label(self.root, text="TIME : ")
        label_time = tk.Label(self.root, text="", )
        label_timer_title.grid(row=CD_ROW, column=CD_COL, columnspan=CD_SPAN)
        label_time.grid(row=CD_ROW, column=CD_COl_GIRD, columnspan=CD_SPAN)
        self.timer = timer
        label_time.config(text=str(self.timer) + " is left")
        if self.timer > 0:
            # call countdown again after 1000ms (1s)
            self.root.after(MILISECOND, self.countdown, timer - 1)
        else:
            messagebox.showinfo(END_OF_TIME_TITLE, END_OF_TIME_MSG)
            self.root.destroy()
            main()

    def lable(self):

        space_label = tk.Label(self.root, text="")
        label_score = tk.Label(self.root, text="SCORE : ")
        entry_score = tk.Label(self.root, text=self.score, width=25, borderwidth=5,
                               bg=None)

        label_words_found_title = tk.Label(self.root, text=" Words Found : ")
        word_found_text = str(self.words_found_list).rstrip()[1:-1]
        label_words_found = tk.Label(self.root, text=word_found_text)

        space_label.grid(row=27, column=12)
        space_label.grid(row=29, column=12)

        label_score.grid(row=18, column=11, columnspan=2)
        entry_score.grid(row=18, column=13, columnspan=2)
        label_words_found_title.grid(row=28, column=12, columnspan=2)
        label_words_found.grid(row=29, column=10, columnspan=4)

    def gui_manager(self):
        self.button_maker()
        self.lable()

    def reset_button(self):
        self.user_pressed_send(None)

    def button_maker(self):
        button_list = []
        letter_list = self.get_letters()
        player_input = tk.Entry(self.root, width=55, borderwidth=5)
        player_input.grid(row=25, column=11, columnspan=4)
        button_send = tk.Button(self.root, text="SEND", command=lambda
            var=player_input: self.user_pressed_send(var))
        button_reset = tk.Button(self.root,text=RESET_BUTTON,command=
        self.reset_button)
        button_reset.grid(row=26, column=13, columnspan=2)
        button_send.grid(row=26, column=11, columnspan=2)
        for i in range(len(letter_list)):
            button = tk.Button(self.root, text=letter_list[i],
                               command=lambda i=i: self.button_press_manager(i,
                                                                             player_input),
                               bg='purple', padx=BUTTON_SIZE_X,
                               pady=BUTTON_SIZE_Y)
            button_list.append(button)
        row_adder = ROW_ADDER
        col_adder = COL_ADDER
        for row in range(len(button_list)):
            if row % BORD_SIZE == 0:
                row_adder += 1
                col_adder = COL_ADDER - 10
            col_adder += 1
            button_list[row].grid(row=row_adder, column=col_adder)

        self.main_board = button_list

    def user_pressed_send(self, player_input):
        path_len = len(self.button_pressed)
        self.button_pressed = []
        if not player_input:
            self.gui_manager()
            return
        word_now = player_input.get()
        if word_now in self.words_found_list:
            pass
        elif word_now in self.words_list:
            score_to_add = path_len ** 2
            self.score += score_to_add
            self.words_found_list.append(word_now)
            player_input.delete(0, tk.END)
        self.gui_manager()

    def button_matrix(self, main_board):
        matrix_main_board = []
        temp_board = []
        counter = 0
        for i in range(len(main_board)):
            temp_board.append(main_board[i])
            if (i + 1) % BORD_SIZE == 0:
                matrix_main_board.append(temp_board)
                temp_board = []
                counter = 0
            counter += 1
        return matrix_main_board

    def button_press_manager(self, letter_index, player_input):
        letter_list = self.get_letters()
        current = player_input.get()
        player_input.delete(0, tk.END)
        player_input.insert(0, str(current) + str(letter_list[letter_index]))
        button_matrix = self.button_matrix(self.main_board)
        pressed_poss = (letter_index // BORD_SIZE, letter_index % BORD_SIZE)
        self.button_pressed.append(pressed_poss)

        for i in range(len(button_matrix)):
            for j in range(len(button_matrix[i])):
                if not ex12_utils.points_distance(pressed_poss[0],
                                                  pressed_poss[1], i, j) or \
                        (i, j) in self.button_pressed:
                    button_matrix[i][j]["state"] = "disabled"
                else:
                    button_matrix[i][j]["state"] = "active"


def main():
    root = tk.Tk()
    if tk.messagebox.askquestion(BEGGINING_TITLE, BEGGINING_MSG) == "yes":
        s = Ui(root, "boggle_dict.txt")
        root.mainloop()


if __name__ == '__main__':
    main()
