"""
TODO Input Sanatisation
TODO History
TODO Layout
"""

import tkinter as tk
import tkinter.scrolledtext as tkst
import numpy as np
from processes.dictionary import Dictionary, compact_letters, compute_letters


MINIMUM_CONSONANTS = 4
MINIMUM_VOWELS = 3
LETTER_TOTAL = 9
START_TIME = 30
NUMBER_OF_ROUNDS = 4

class Main(tk.Tk):
    def __init__(self):
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
        self.build_ui()
        self.history = "Round 1"
    
    def build_ui(self):
        self.title("Countdown")
        self.geometry('400x600')
        self.explaination = tk.Label(self, text='Explaination text')
        self.explaination.pack()
        self.score_label = tk.Label(self, text='Score: 0')
        self.score_label.pack()
        self.round_label = tk.Label(self, text='Round: 1')
        self.round_label.pack()
        self.timer_label = tk.Label(self, text=f'{self.time}s')
        self.timer_label.pack()
        self.selected_elements = tk.Label(self, text='')
        self.selected_elements.pack()
        self.vowel_button = tk.Button(self, text="Vowel", command=self.add_vowel)
        self.vowel_button.pack()
        self.consonant_button = tk.Button(self, text="Consonant", command=self.add_consonant)
        self.consonant_button.pack()
        self.word_box = tk.Text(self, height=1, width=9)
        self.word_box.pack()
        self.next_round_button = tk.Button(self, text="Next Round", command=self.next_round)
        self.next_round_button.pack()
        self.next_round_button['state']
        self.new_game_button = tk.Button(self, text="New Game", command=self.new_game)
        self.new_game_button.pack()
        #need to limit input to maximum 9 characters
        self.close_button = tk.Button(self, text="Close", command=lambda: self.destroy())
        self.close_button.pack()
        self.history_label = tkst.ScrolledText(self)
        self.history_label.pack()
        self.history_label.insert(tk.INSERT, "Round 1\n")
        self.history_label.configure(state = "disabled")

    def add_to_history(self, text):
        self.history_label.configure(state = "normal")
        self.history_label.insert(tk.INSERT, text+"\n")
        self.history_label.configure(state = "disabled")
    
    def new_game(self):
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
        game_letters = compute_letters(self.letters)
        longest_words = self.dictionary.find_longest_word(game_letters)
        player_word = self.word_box.get('0.0', 'end').strip()
        #check if player word only contains letters, remove uppercase
        player_letters = compute_letters(player_word)
        string = f"Player Word: {player_word},"
        if np.any(game_letters - player_letters < 0):
            string += ' invalid letters, Word Score: 0'
        elif player_word not in self.dictionary.word_set:
            string += ' input not a word, Word Score: 0'
        else:
            score = len(player_word)
            if score == LETTER_TOTAL:
                score *= 2
            string += f' valid word, Word Score: {score}'
            self.score += score
            self.score_label['text'] = f"Score: {self.score}"
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
        self.game_loop()
        self.add_to_history(f"Letters {''.join(self.letters)}")

    def game_loop(self):
        self.time -= 1
        self.timer_label['text'] = f"{self.time}s"
        if self.time > 0:
            self.after(1000, self.game_loop)
        else:
            self.end_game()
    
    def display_letters(self):
        string = "".join(self.letters)
        self.selected_elements['text'] = string

    def add_vowel(self):
        self.letters.append(self.dictionary.random_vowel())
        self.vowels += 1
        self.letter_number += 1
        self.display_letters()
        if self.consonants < MINIMUM_CONSONANTS and LETTER_TOTAL - self.letter_number == MINIMUM_CONSONANTS - self.consonants:
            self.vowel_button['state'] = tk.DISABLED
        if LETTER_TOTAL == self.letter_number:
            self.consonant_button['state'] = tk.DISABLED
            self.vowel_button['state'] = tk.DISABLED
            self.start_loop()

    
    def add_consonant(self):
        self.letters.append(self.dictionary.random_consonant())
        self.consonants += 1
        self.letter_number += 1
        self.display_letters()
        if self.vowels < MINIMUM_VOWELS and LETTER_TOTAL - self.letter_number == MINIMUM_VOWELS - self.vowels:
            self.consonant_button['state'] = tk.DISABLED
        if LETTER_TOTAL == self.letter_number:
            self.consonant_button['state'] = tk.DISABLED
            self.vowel_button['state'] = tk.DISABLED
            self.start_loop()

if __name__ == "__main__":
    countdown = Main()
    countdown.mainloop()