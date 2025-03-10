"""
Possible adjustments:
- Better dictionary
- Generate a set collection of words and pull without replacement
- Adjust common letters to that of 9 letter words not the entire collection
- Highscore/saving history
- Record Maximum possible score
"""

import tkinter as tk
import tkinter.scrolledtext as tkst
import numpy as np
import os
from processes.dictionary import Dictionary, compact_letters, compute_letters

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

MINIMUM_CONSONANTS = 4
MINIMUM_VOWELS = 3
LETTER_TOTAL = 9
START_TIME = 30
NUMBER_OF_ROUNDS = 4
EXPLAINATION_FILE = 'explaination.txt'

class Main(tk.Tk):
    def __init__(self):
        """
        Initialise the program
        """
        super().__init__()
        self.dictionary = Dictionary(LETTER_TOTAL)
        self.letter_array = np.zeros(26)
        self.letters = []
        self.vowels = 0
        self.consonants = 0
        self.letter_number = 0
        self.time = START_TIME
        self.score = 0
        self.round = 1
        self.history = "Round 1"
        self.explaintation = ""
        with open(os.path.join(FILE_PATH, EXPLAINATION_FILE)) as file:
            self.explaination = file.read().format(LETTER_TOTAL = LETTER_TOTAL, MINIMUM_CONSONANTS=MINIMUM_CONSONANTS, MINIMUM_VOWELS=MINIMUM_VOWELS, NUMBER_OF_ROUNDS= NUMBER_OF_ROUNDS, START_TIME=START_TIME, TWICE_LETTER_TOTAL= LETTER_TOTAL*2)
        self.build_ui()
    
    def build_ui(self):
        """
        Generate the User Interface
        """
        self.title("Countdown")
        self.explaination = tk.Label(self, text=self.explaination)
        self.explaination.grid(row=0, column=0, columnspan=3)
        self.score_label = tk.Label(self, text='Score: 0')
        self.score_label.grid(row=1, column=0)
        self.round_label = tk.Label(self, text='Round: 1')
        self.round_label.grid(row=1, column=1)
        self.timer_label = tk.Label(self, text=f'Time Left: {self.time}s')
        self.timer_label.grid(row=1, column=2)
        self.selected_elements = tk.Label(self, text='', font=("Arial", 25))
        self.selected_elements.grid(row=2, column=1)
        self.vowel_button = tk.Button(self, text="Vowel", command=self.add_vowel)
        self.vowel_button.grid(row=3, column=0)
        self.consonant_button = tk.Button(self, text="Consonant", command=self.add_consonant)
        self.consonant_button.grid(row=3, column=2)
        self.word_box = tk.Text(self, height=1, width=9)
        self.word_box.grid(row=4, column=1)
        self.next_round_button = tk.Button(self, text="Next Round", command=self.next_round)
        self.next_round_button.grid(row=5, column=0)
        self.next_round_button['state']
        self.new_game_button = tk.Button(self, text="New Game", command=self.new_game)
        self.new_game_button.grid(row=5, column=1)
        self.close_button = tk.Button(self, text="Close", command=lambda: self.destroy())
        self.close_button.grid(row=5, column=2)
        self.history_label = tkst.ScrolledText(self)
        self.history_label.grid(row=6, column=0, columnspan=3)
        self.history_label.insert(tk.INSERT, "Round 1\n")
        self.history_label.configure(state = "disabled")

    def add_to_history(self, text):
        """
        Subfunction to add to the program history
        """
        self.history_label.configure(state = "normal")
        self.history_label.insert(tk.INSERT, text+"\n")
        self.history_label.configure(state = "disabled")
        self.history_label.see('end')
    
    def new_game(self):
        """
        Resets the program for the user to play again
        """
        self.letter_array = np.zeros(26)
        self.letters = []
        self.vowels = 0
        self.consonants = 0
        self.letter_number = 0
        self.time = START_TIME
        self.score = 0
        self.round = 1
        self.timer_label['text']=f'{self.time}s'
        self.round_label['text']=f'Round: {self.round}'
        self.selected_elements['text'] = ''
        self.consonant_button['state'] = tk.NORMAL
        self.vowel_button['state'] = tk.NORMAL
        self.word_box.delete('0.0', 'end')
        self.next_round_button['state'] = tk.DISABLED
        self.add_to_history(f"")
        self.add_to_history(f"New Game")
        self.add_to_history(f"Round {self.round}")

    def next_round(self):
        """
        Progresses the game to the next round
        """
        self.round += 1
        self.letter_array = np.zeros(26)
        self.letters = []
        self.vowels = 0
        self.consonants = 0
        self.letter_number = 0
        self.time = START_TIME
        self.timer_label['text']=f'{self.time}s'
        self.round_label['text']=f'Round: {self.round}'
        self.selected_elements['text'] = ''
        self.consonant_button['state'] = tk.NORMAL
        self.vowel_button['state'] = tk.NORMAL
        self.word_box.delete('0.0', 'end')
        self.next_round_button['state'] = tk.DISABLED
        self.add_to_history(f"Round {self.round}")


    def end_game(self):
        """
        Computes the longest possible words and checks the players word at the end of a round
        """
        game_letters = compute_letters(self.letters)
        longest_words = self.dictionary.find_longest_word(game_letters)
        player_word = self.word_box.get('0.0', 'end').strip().lower()
        string = f"Player Word: {player_word},"
        if player_word.isalpha():
            player_letters = compute_letters(player_word)
            #processing and displaying in history the round
            if np.any(game_letters - player_letters < 0):
                string += ' invalid letters, Word Score: 0'
            elif player_word not in self.dictionary.word_set:
                string += ' input not a word, Word Score: 0'
            else:
                score = len(player_word)
                if score == LETTER_TOTAL:
                #so that the player scores double (18 if 9 letters) when they get the maximum length word
                    score *= 2
                string += f' valid word, Word Score: {score}'
                self.score += score
                self.score_label['text'] = f"Score: {self.score}"
        else:
            string += ' contains non-alphabet characters, Word Score: 0'
        self.add_to_history(string)
        if len(longest_words) > 1:
            self.add_to_history(f"Longest posible words: {', '.join(longest_words)}")
        else:
            self.add_to_history(f"Longest posible word: {list(longest_words)[0]}")
        if self.round < NUMBER_OF_ROUNDS:
            self.next_round_button['state'] = tk.NORMAL
        else:
            self.add_to_history(f"GAME OVER SCORE: {self.score}")

        

    def start_loop(self):
        """
        Starts the gameloop
        """
        self.game_loop()
        self.add_to_history(f"Letters {''.join(self.letters)}")

    def game_loop(self):
        """
        Reduces the timer calling itself until the time is finished
        """
        self.time -= 1
        self.timer_label['text'] = f"Time Left: {self.time}s"
        if self.time > 0:
            self.after(1000, self.game_loop)
        else:
            self.end_game()
    
    def display_letters(self):
        """
        Displays the letters
        """
        string = "".join(self.letters)
        self.selected_elements['text'] = string

    def add_vowel(self):
        """
        Adds a vowel to the letter list
        """
        self.letters.append(self.dictionary.random_vowel())
        self.vowels += 1
        self.letter_number += 1
        self.display_letters()
        #the following enables and disables buttons depending on whether there are enough letters or if the rest of the letters need to be consonants
        if self.consonants < MINIMUM_CONSONANTS and LETTER_TOTAL - self.letter_number == MINIMUM_CONSONANTS - self.consonants:
            self.vowel_button['state'] = tk.DISABLED
        if LETTER_TOTAL == self.letter_number:
            self.consonant_button['state'] = tk.DISABLED
            self.vowel_button['state'] = tk.DISABLED
            self.start_loop()

    
    def add_consonant(self):
        """
        Adds a consonant to the letter list
        """
        self.letters.append(self.dictionary.random_consonant())
        self.consonants += 1
        self.letter_number += 1
        self.display_letters()
        #the following enables and disables buttons depending on whether there are enough letters or if the rest of the letters need to be vowel
        if self.vowels < MINIMUM_VOWELS and LETTER_TOTAL - self.letter_number == MINIMUM_VOWELS - self.vowels:
            self.consonant_button['state'] = tk.DISABLED
        if LETTER_TOTAL == self.letter_number:
            self.consonant_button['state'] = tk.DISABLED
            self.vowel_button['state'] = tk.DISABLED
            self.start_loop()

if __name__ == "__main__":
    countdown = Main()
    countdown.mainloop()