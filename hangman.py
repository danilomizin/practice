# Problem Set 2, hangman.py
# Name:Mizin Danilo
# Collaborators:Piustonen
# Time spent:

import string
import random


WORDLIST_FILENAME = "words.txt"
LIST_VOWELS = frozenset("aeiou")


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
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
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass


def warnings(value_mistake, warnings_point, guesses_point):
    """
    Subtract warnings point and output name of error
    """
    name_mistake = f"Oops! {value_mistake}"
    if warnings_point > 0:
        warnings_point -= 1
        print(name_mistake, "\nYou have", warnings_point, "warnings left:", end=" ")
    else:
        guesses_point -= 1
        print("Oops! You have no warnings left, so you lose one guess:", end=' ')
    return warnings_point, guesses_point


def check_star_30(count, secret_word, letters_guessed):
    pass


def letter_in_word(secret_word, letter, list_vowels, letter_guessed, guesses_point, letters_guessed):
    """
    Check if letter is word, else subtracts point
    """
    letters_guessed.append(letter)
    if letter in secret_word:
        print("Good guess:", get_guessed_word(secret_word, letters_guessed))
    else:
        if letter in list_vowels:
            guesses_point -= 2
        else:
            guesses_point -= 1
        print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
    return letters_guessed, guesses_point


def classic_input(count_star, warnings_point, guesses_point):
    if count_star != 0:
        warnings_point, guesses_point = warnings("you are playing classic hangman", warnings_point, guesses_point)
    else:
        print("OOps, you are playing classic hangman:", end=" ")
        count_star += 1
    return warnings_point, guesses_point, count_star


def hangman(secret_word, request, list_vowels, warnings_point, letters_guessed, guesses_point, count_star):
    '''
    Game Hangman. "request" show hangman(classic) or hangman with hints.
    Print information for user, start loop, check user choose hangman or hangman with hints,
    Check input letter and call letter_in_word, check if user guessed word.
    '''
    print("I am thinking of a word that is", len(secret_word), "letters long")
    print("You have", warnings_point, "warnings left")
    while guesses_point > 0:
        print("-------")
        print("You have", guesses_point, "guesses left")
        print("Available letters:", end=" ")
        get_available_letters(letters_guessed)
        letter = input("Please guess a letter:")
        if request == "hints" and letter == "*":
            check_star_30(count_star, secret_word, letters_guessed)
            count_star += 1
        else:
            if letter == "*":
                warnings_point, guesses_point, count_star = classic_input(count_star, warnings_point, guesses_point)
                print(get_guessed_word(secret_word, letters_guessed))
            elif letter not in string.ascii_letters or len(letter) != 1:
                warnings_point, guesses_point = warnings("That is not a valid letter or you print more than one letter.", warnings_point, guesses_point)
                print(get_guessed_word(secret_word, letters_guessed))
            elif letter in letters_guessed:
                warnings_point, guesses_point = warnings("You have already guessed that letter:", warnings_point, guesses_point)
                print(get_guessed_word(secret_word, letters_guessed))
            else:
                letters_guessed, guesses_point = letter_in_word(secret_word, letter, LIST_VOWELS, letters_guessed, guesses_point, letters_guessed)
        if is_word_guessed(secret_word, letters_guessed) == 0 or guesses_point <= 0:
            break
    if is_word_guessed(secret_word, letters_guessed) == 0:
        final_points = guesses_point*len(set(secret_word))
        print("------")
        print("Congratulations, you won!")
        print("Word:", secret_word)
        print("Your total score for this game is:", final_points)
    elif is_word_guessed(secret_word, letters_guessed) != 0 and guesses_point <= 0:
        print("------")
        print("Sorry, you ran out of guessed. The word was", secret_word)


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    my_word = my_word.replace(" ", "")
    if len(my_word) == len(other_word):
        for i in range(len(my_word)):
            if (my_word[i] != '_' and my_word[i] != other_word[i]) or (my_word[i] == "_" and other_word[i] in my_word):
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
    for word in list(wordlist):
        if match_with_gaps(my_word, word) is True:
            list_with_words.append(word)
    print("Possible word matches are:", " ".join(list_with_words))


def start(guesses_point, warnings_point, letters_guessed, count_star):
    print("Welcome to the game Hangman!\nDo you want play hangman (classic) or hangman with hints?")
    while type:
        request = input("if you want to play hangman (classic) input 'classic', play hangman with hints input 'hints':").replace(" ", "")
        if request == "classic" or request == "hints":
            secret_word = choose_word(wordlist)
            hangman(secret_word, request, LIST_VOWELS, warnings_point, letters_guessed, guesses_point, count_star)
            break
        else:
            print("Oops! Your input is not correct")


if __name__ == "__main__":
    count_star = 0
    guesses_point = 6
    warnings_point = 3
    letters_guessed = []
    start(guesses_point, warnings_point, letters_guessed, count_star)