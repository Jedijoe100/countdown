import numpy as np
import os
import time

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DICTIONARY_PATH = "../dictionary"

class Dictionary:
    def __init__(self, num_letters):
        """
        Loads and processes the dictionary into a usable format for countdown
        """
        self.rng = np.random.default_rng()
        self.num_letters = num_letters
        self.letter_count = np.zeros(26)
        self.word_dictionary = {}
        self.word_set = set()
        start = time.time()
        self.load_words('words_alpha.txt')        
        print(f"Dictionary load time: {time.time()- start}s")
        #get proportion of consinants and vowels
        self.vowel_index = np.array([0, 4, 8, 14, 20])
        self.vowel_distribution = self.letter_count[self.vowel_index]/np.sum(self.letter_count[self.vowel_index])
        self.consonant_index = np.delete(np.arange(0, 26), self.vowel_index)
        self.consonant_distribution =self.letter_count[self.consonant_index]/np.sum(self.letter_count[self.consonant_index])
        print(self.vowel_distribution, self.consonant_distribution)
        
    def find_longest_word(self, letters):
        """
        Iteratively finds the longest word(s) from the given letters
        """
        letter_index = np.where(letters>0)[0]
        permutations = [letters]
        new_permutations = []
        is_found = False
        found_words = set()
        while not is_found:
            for value in permutations:
                test = self.word_dictionary.get(compact_letters(value), (-1,))
                if test[0] != -1:
                    is_found = True
                    found_words.update(test)
                elif not is_found:
                    for index in letter_index:
                        if value[index] > 0:
                            new_value = value.copy()
                            new_value[index] -= 1
                            new_permutations.append(new_value)
            permutations = new_permutations.copy()
            new_permutations = []
        return found_words
    
    def random_vowel(self):
        """
        Randomly selects a vowel according to it's natural abundance within the set of words
        """
        num = self.rng.choice(self.vowel_index, p=self.vowel_distribution)
        return chr(97 + num)
    
    def random_consonant(self):
        """
        Randomly selects a consonant according to it's natural abundance within the set of words
        """
        num = self.rng.choice(self.consonant_index, p=self.consonant_distribution)
        return chr(97 + num)
    
    def load_words(self, filename):
        """
        Loads the words given a filename
        """
        with open(os.path.join(FILE_PATH, DICTIONARY_PATH, filename)) as file:
            for line in file.readlines():
                word = line.strip()
                if len(word) <= self.num_letters:
                    letter_count_array = compute_letters(word)
                    letter_count_string = compact_letters(letter_count_array)
                    current_array = self.word_dictionary.get(letter_count_string, [])
                    current_array.append(word)
                    self.word_dictionary[letter_count_string] = current_array
                    self.word_set.add(word)
                    self.letter_count += letter_count_array

def compact_letters(letter_array):
    string = ""
    for i in range(0, 26):
        string += str(letter_array[i])
    return string

def compute_letters(word):
    """
    Returns an array of how many of each character are in a word
    """
    letters = np.zeros(26)
    for letter in word:
        letters[ord(letter) - 97] += 1 #97 is the ASCII code for 'a'
    return letters

if __name__ == '__main__':
    dictionary = Dictionary(9)