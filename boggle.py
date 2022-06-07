from tkinter import messagebox
import boggle_board_randomizer
import tkinter as tk
import ex12_utils
import pygame

# Game configuration:
BORD_SIZE = 4
GAME_TIME = 180
INITIAL_SCORE = 0

# count down arg
CD_ROW = 17
CD_COL = 11
CD_SPAN = 2
CD_COl_GIRD = 13

# lable
WELCOME_MSG = "Welcome to the boggle"
YOUR_SCORE = " Your score is: "

# BUTTON
BUTTON_WIDTH = 13
BUTTON_HEIGHT = 4

WIDTH_ENTRY = 35
BORDER_WIDTH_ENTRY = 5
INPUT_GRID_ROW = 50
INPUT_GRID_COL = 10
COL_SPAN = 10
ROW_ADDER = 20
COL_ADDER = 20
MILISECOND = 1000

# msg
BEGGINING_MSG = "Hey there, would you like to play a game?"
BEGGINING_TITLE = "Welcome menu"
END_OF_TIME_TITLE = "Time Over"
END_OF_TIME_MSG = "Time is over"

RESET_BUTTON = "Reset"


# atary added end

# boggle_board_randomizer.randomize_board()

class Ui:
    """
    This is a boggle game class, containing user interface functions using python gui
    and game play data according to boggle game rules as given in ex12 instructions.

    $$$ - adam - maybe we should change the class name to something more general

    """

    def __init__(self, root, words_path):
        """
        This is the class constructor function, it contains the gameplay data, which is updating as the game develops.
        :param root: tkinter as tk - for gui
        :param words_path: name for list of words file, given in additional files as 'boggle_dict.txt'
        """
        self.board_list = boggle_board_randomizer.randomize_board()
        self.words_list = ex12_utils.list_from_words_file(words_path)
        self.score = INITIAL_SCORE
        self.timer = GAME_TIME
        self.main_board = []
        self.root = root
        self.button_pressed = []
        self.words_found_list = []
        self.gui_manager()
        self.countdown(self.timer)

    def get_letters(self):
        """
        This function returns all the letters in board list, if a cell in the boggle board contains more than
        a single letter, it will append it to the letter_list as a string of more than 1 character.
        :return: letter_list - list of every cell data in board.
        """
        letter_list = []
        for i in range(len(self.board_list)):
            for j in range(len(self.board_list[i])):
                letter_list.append(self.board_list[i][j])
        return letter_list

    def countdown(self, timer):
        """
        This function is build for the game timer, starting from 180 seconds (3 minutes following ex12 instructions)
        it updates the game timer with every 1000ms (every second) passing.
        :param timer: game current time (default from 180 seconds)
        :return: None
        """
        label_timer_title = tk.Label(self.root, text="TIME: ", font=12, bg="grey")
        label_time = tk.Label(self.root, text="", )
        label_timer_title.grid(row=CD_ROW, column=CD_COL, columnspan=CD_SPAN)
        label_time.grid(row=CD_ROW, column=CD_COl_GIRD, columnspan=CD_SPAN)
        self.timer = timer
        label_time.config(text=str(self.timer) + " is left", font=9)
        if self.timer > 0:
            # call countdown again after 1000ms (1s)
            self.root.after(MILISECOND, self.countdown, timer - 1)
        else:
            messagebox.showinfo(END_OF_TIME_TITLE, END_OF_TIME_MSG + YOUR_SCORE
                                + str(self.score))
            self.root.destroy()
            main()

    def lable(self):
        """
        This function contains all the labels presented on the boggle game screen using grid geometric gui platform.
        it is called with every time the user is pressing SEND button.
         if the user has found a word, calling this function will update the game score and the list of words found.
        :return: None
        """
        # sound button
        sound_button = tk.Button(self.root, text="Start/stop \n music", command=self.sound_button, height=5, width=10,
                                 bg="grey")
        sound_button.grid(row=29, column=13, columnspan=2)

        # creating labels
        space_label = tk.Label(self.root, text="")
        label_score = tk.Label(self.root, text="SCORE : ", bg="grey", font=12)
        entry_score = tk.Label(self.root, text=self.score, width=25, borderwidth=5, bg=None, font=9)
        label_words_found_title = tk.Label(self.root, text=" Words Found : ", bg="grey", font=16)
        word_found_text = str(self.words_found_list).rstrip()[1:-1].replace("'", "")
        label_words_found = tk.Label(self.root, text=word_found_text, font=13)
        welcome_to_the_boggel = tk.Label(self.root, text=WELCOME_MSG, fg="gray25", font=8)

        # placing labels on screen with grid
        space_label.grid(row=27, column=12)
        space_label.grid(row=29, column=12)
        label_score.grid(row=18, column=11, columnspan=2)
        welcome_to_the_boggel.grid(row=18, column=14, columnspan=2)
        entry_score.grid(row=18, column=13, columnspan=2)
        label_words_found_title.grid(row=36, column=4, columnspan=10)
        label_words_found.grid(row=37, column=1, columnspan=20)

    def sound_button(self):
        pygame.mixer.init()
        sound = pygame.mixer.Sound("surprise_sound.mp3")
        if pygame.mixer.get_busy():
            pygame.mixer.stop()
        else:
            pygame.mixer.Sound.play(sound)
        # This is the sound channel

    def gui_manager(self):
        """
        This function is called with every game move - pressing
        :return:
        """
        self.button_maker()
        self.lable()

    def reset_button(self):
        self.user_pressed_send(None)

    def button_maker(self):
        """
        This function build and updates the boggle board buttons with their data (letters).
        it also build and updates the board buttons - send, reset, and the user input box for selected board path.
        :return: None
        """
        button_list = []
        letter_list = self.get_letters()

        player_input = tk.Entry(self.root, width=55, borderwidth=5)
        button_send = tk.Button(self.root, text="SEND", command=lambda
            var=player_input: self.user_pressed_send(var), bg="grey", height=5, width=10)
        button_reset = tk.Button(self.root, text=RESET_BUTTON, command=
        self.reset_button, height=5, width=10, bg="grey")

        player_input.grid(row=28, column=12, columnspan=4)
        button_reset.grid(row=29, column=14, columnspan=2)
        button_send.grid(row=29, column=12, columnspan=2)

        # creating and updating the board buttons

        for i in range(len(letter_list)):
            button = tk.Button(self.root, text=letter_list[i],
                               command=lambda i=i: self.button_press_manager(i,
                                                                             player_input),
                               bg="DarkSlateGray4", width=BUTTON_WIDTH,
                               height=BUTTON_HEIGHT, font=15)
            button_list.append(button)
        row_adder = ROW_ADDER
        col_adder = COL_ADDER
        for row in range(len(button_list)):
            if row % BORD_SIZE == 0:
                row_adder += 1
                col_adder = COL_ADDER - 9
            col_adder += 1
            button_list[row].grid(row=row_adder, column=col_adder)

        self.main_board = button_list

    def user_pressed_send(self, player_input):
        """
        This function is called when user pressed SEND button. (called from button widget)
        :param player_input: the string compound from the user seleceted letters on the boggle board, as shown
        in the game entry.
        if the string in the entry when the user pressed SEND is a valid word = in the words list and was not found
        before, the user will be added score correspondingly to ex12 game rules, and this word will be appended
        to the game attribute - list of words founded.
        :return: None
        """
        path_len = len(self.button_pressed)
        self.button_pressed = []
        if not player_input:
            self.gui_manager()
            return
        word_now = player_input.get()
        if word_now in self.words_found_list:
            self.gui_manager()
        elif word_now in self.words_list:
            score_to_add = path_len ** 2
            self.score += score_to_add
            self.words_found_list.append(word_now)
            player_input.delete(0, tk.END)
        self.gui_manager()

    def button_matrix(self, main_board):
        """
        here we will transform the list to a matrix
        :param main_board:
        :return:
        """
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
        """
        by getting a press from the player we will disable the button that we
        dont want to him to press
        :param letter_index:
        :param player_input:
        :return:
        """
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
                    button_matrix[i][j]["bg"] = "misty rose"
                else:
                    button_matrix[i][j]["state"] = "active"
                    button_matrix[i][j]["fg"] = "yellow"
                    button_matrix[i][j]["bg"] = "DarkSlateGray4"


def main():
    root = tk.Tk()
    root.resizable(False, False)

    if tk.messagebox.askquestion(BEGGINING_TITLE, BEGGINING_MSG) == "yes":
        s = Ui(root, "boggle_dict.txt")
        root.mainloop()
    else:
        root.destroy()

if __name__ == '__main__':
    main()
