# Problem Set 2, hangman.py
# Name:Mizin Danilo
# Collaborators:Piustonen
# Time spent:

import string
import random


WORDLIST_FILENAME = "words.txt"
LIST_VOWELS = "aeiou"
HINTS_SYMBOL = "*"
HIDDEN_LETTER = "_"
GUESSES_POINT = 6
WARNINGS_POINT = 3


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")

    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letters in secret_word:
        if letters not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    formed_word = []
    for i in range(len(secret_word)):
        if secret_word[i] in letters_guessed:
            formed_word.append(secret_word[i])
        else:
            formed_word.append(HIDDEN_LETTER)

    return ' '.join(formed_word)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    letters = string.ascii_lowercase
    for symbol in letters_guessed:
        letters = letters.replace(symbol, '')
    return letters


def warnings(value_mistake, warnings_point, guesses_point, secret_word, letters_guessed):
    """
    Subtract warnings point and output name of error
    'value_mistake' is name of mistake.
    'secret_word' is random word, which user need to guess.
    'letters_guessed' is set of letters, which user guessed.
    """
    if warnings_point > 0:
        warnings_point -= 1
        print(f"Oops! {value_mistake}")
        print(f"You have {warnings_point} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
    else:
        #if user does not have a warnings points, he\she lose one guesses point
        guesses_point -= 1
        print("Oops! You have no warnings left, so you lose one guess:"
              f" {get_guessed_word(secret_word, letters_guessed)}")

    return warnings_point, guesses_point


def print_hints_warning(list_word):
    """
    function finds words that matches with letters which were chosen by user earlier
    :param list_word: list of word attached with game
    """
    if len(list_word) < 30:

        print("Possible word matches are:", " ".join(list_word))
    else:
        print("Possible word matches are:", " ".join(list_word[0:30]))


def letter_in_word(secret_word, letter, guesses_point, letters_guessed):
    """
    Check if letter is word, else subtracts point.
    'secret_word' is random word, which user need to guess.
    'letter' is letter, which user inputted
    'letters_guessed' is set of letters, which user guessed.
    """
    letters_guessed.add(letter)
    if letter in secret_word:
        print("Good guess:", get_guessed_word(secret_word, letters_guessed))
    else:
        if letter in LIST_VOWELS:
            guesses_point -= 2
        else:
            guesses_point -= 1
        print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))

    return letters_guessed, guesses_point


count_star = 0


def print_classic_warning(warnings_point, guesses_point, secret_word, letters_guessed):
    '''
    If user is playing in classic game, but inputted '*', firstly programme output information
    that user is playing in classic game, next time if user will input '*' he/she will lose
    one warnings point
    'secret_word' is random word, which user need to guess.
    'letters_guessed' is set of letters, which user guessed.
    'count_star' is variable, which count how many times user input '*'
    '''
    global count_star
    if count_star != 0:
        warnings_point, guesses_point = warnings("you are playing classic hangman", warnings_point,
                                                 guesses_point, secret_word, letters_guessed)
    else:
        print("Oops, you are playing classic hangman:", get_guessed_word(secret_word, letters_guessed))
        count_star += 1

    return warnings_point, guesses_point


def check_letter(letter, warnings_point, guesses_point, secret_word, letters_guessed):
    '''
    This function check if letter is correct. So letter is correct, if it is acsii_letters, len(letter) is 1 and
    letter not in letters_guessed. Additionally, it check that letter is or is not a HINTS_SYMBOL("*")
    'secret_word' is random word, which user need to guess.
    'letter' is letter, which user inputted
    'letters_guessed' is set of letters, which user guessed.
    '''

    if letter == HINTS_SYMBOL:
        warnings_point, guesses_point = print_classic_warning(warnings_point, guesses_point,
                                                              secret_word, letters_guessed)
    elif letter not in string.ascii_letters or len(letter) != 1:
        warnings_point, guesses_point = warnings("That is not a valid letter or you print more than one letter.",
                                                 warnings_point, guesses_point, secret_word, letters_guessed)
    elif letter in letters_guessed:
        warnings_point, guesses_point = warnings("You have already guessed that letter:",
                                                 warnings_point, guesses_point, secret_word, letters_guessed)
    else:
        letters_guessed, guesses_point = letter_in_word(secret_word, letter, guesses_point, letters_guessed)

    return warnings_point, guesses_point


def result_of_game(secret_word, letters_guessed, guesses_point):
    '''
    This functions output information, if user win or lose.
    If user win, output information about points, which user earn.
    If user lose, output information and show secret word.
    'secret_word' is random word, which user need to guess.
    'letters_guessed' is set of letters, which user guessed.
    '''
    if is_word_guessed(secret_word, letters_guessed):
        final_points = guesses_point * len(set(secret_word))
        print("------")
        print("Congratulations, you won!")
        print("Word:", secret_word)
        print("Your total score for this game is:", final_points)

    elif guesses_point <= 0:
        print("------")
        print("Sorry, you ran out of guessed. The word was", secret_word)


def hangman(secret_word, with_hints):
    '''
    Game Hangman. "request" show hangman(classic) or hangman with hints.
    Print information for user, start loop, check user choose hangman or hangman with hints,
    Check input letter and call letter_in_word, check if user guessed word.
    'secret_word' is random word, which user need to guess.
    'with_hints' is a bool variable, show, which type of game user chose.
    '''

    guesses_point = GUESSES_POINT
    warnings_point = WARNINGS_POINT
    letters_guessed = set()
    print(f"I am thinking of a word that is {len(secret_word)} letters long")
    print(f"You have {WARNINGS_POINT} warnings left")

    while guesses_point > 0 and not is_word_guessed(secret_word, letters_guessed):
        print("-------")
        print(f"You have {guesses_point} guesses left")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        letter = input("Please guess a letter:")

        if with_hints and letter == HINTS_SYMBOL:
            #print list of words, which are possible matches with secret_word
            show_possible_matches(get_guessed_word(secret_word,letters_guessed))
        else:
            warnings_point, guesses_point = check_letter(letter, warnings_point, guesses_point,
                                                         secret_word, letters_guessed)
    #output information about result of game
    result_of_game(secret_word, letters_guessed, guesses_point)


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    if len(my_word) == len(other_word):
        for letter_my, letter_other in zip(my_word, other_word):
            if (letter_my != HIDDEN_LETTER and letter_my != letter_other) or \
                    (letter_my == HIDDEN_LETTER and letter_other in my_word):
                return False
        return True
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    list_with_words = []
    my_word = my_word.replace(" ", "")
    for word in wordlist:
        if match_with_gaps(my_word, word):
            list_with_words.append(word)

    #check if length of list_with_words <30 or>30
    print_hints_warning(list_with_words)


def user_wants_hints():
    '''
    This function ask user about type of game. Return True if hints and False if classic.
    '''
    print("Welcome to the game Hangman!")
    print("Do you want play hangman (classic) or hangman with hints?")
    is_hints_input_valid = True
    while is_hints_input_valid:
        type_of_game = input("if you want to play hangman (classic) input 'classic',"
                             " play hangman with hints input 'hints':").strip()
        if type_of_game == "classic":
            is_hints_input_valid = False
            return is_hints_input_valid
        elif type_of_game == "hints":
            return is_hints_input_valid
        else:
            print("Oops! Your input is not correct.")


if __name__ == "__main__":
    with_hints = user_wants_hints()
    secret_word = choose_word(wordlist)
    hangman(secret_word, with_hints)
