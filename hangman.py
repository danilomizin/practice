# Problem Set 2, hangman.py
# Name:Mizin Danilo
# Collaborators:Piustonen 
# Time spent:

import string
import random

WORDLIST_FILENAME = "words.txt"
guesses_point=6
warnings_point=3
letters_guessed=[]


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


wordlist = load_words()


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    counter = 0
    flag = False
    for letter_s in secret_word:
        for letter_lg in letters_guessed:
            if letter_s == letter_lg:
                flag = True
                break
        if not flag:
            counter += 1
        flag = False
    return counter


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    my_word=[]
    for i in range(len(secret_word)):
        if secret_word[i] in letters_guessed:
             my_word.append(secret_word[i])
        else:
            my_word.append("_ ")
    return "".join(my_word)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    if len(letters_guessed)==0:
        x =string.ascii_lowercase
        return x
    else:
        z =list(string.ascii_lowercase)
        for letter in letters_guessed:
            del z[z.index(letter.lower())]
        return ''.join(z)


def warnings(value_error):
    """
    Subtract warnings point and output name of error
    """
    global warnings_point
    global guesses_point
    format_error="Oops! {}".format(value_error)
    if warnings_point>0:
        warnings_point-=1
        print(format_error,"\nYou have", warnings_point, "warnings left:",end=" ")

    else:
        guesses_point-= 1
        print("Oops! You have no warnings left, so you lose one guess:", end=' ')


def letter_in_word(secret_word,letter,letters_a):
    """
    Check if letter is word, else subtracts point
    """
    global letter_guessed
    global guesses_point
    letters_guessed.append(letter)
    if letter in secret_word:
        print("Good guess:", get_guessed_word(secret_word, letters_guessed))
    else:
        if letter in letters_a:
            guesses_point -= 2
        else:
            guesses_point -= 1
        print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))


def hangman(secret_word, request):
    '''
    Game Hangman. "request" show hangman(classic) or hangman with hints.
    Print information for user, start loop, check user choose hangman or hangman with hints,
    Check input letter and call letter_in_word, check if user guessed word.
    '''
    global letters_guessed
    global warnings_point
    global guesses_point
    letters_a = frozenset("aeiou")
    print("I am thinking of a word that is", len(secret_word), "letters long")
    print("You have", warnings_point, "warnings left")
    while guesses_point > 0:
        print("-------\nYou have", guesses_point, "guesses left\nAvailable letters:", end=" ")
        print(get_available_letters(letters_guessed))
        letter = input("Please guess a letter:")
        if request == "hints" and letter=="*":
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        else:
            if str.isalpha(letter.lower()) == False or len(letter) != 1:
                warnings("That is not a valid letter or you print more than one letter.")
                print(get_guessed_word(secret_word, letters_guessed))
            elif letter in letters_guessed:
                warnings("You have already guessed that letter:")
                print(get_guessed_word(secret_word, letters_guessed))
            else:
                letter_in_word(secret_word, letter, letters_a)
        if is_word_guessed(secret_word, letters_guessed) == 0:
            final_points = guesses_point * len(set(secret_word))
            print("------\nCongratulations, you won!\nWord:",secret_word,"\nYour total score for this game is:", final_points)
            guesses_point = -1
        elif is_word_guessed(secret_word, letters_guessed) != 0 and guesses_point <= 0:
            print("------\nSorry, you ran out of guessed. The word was", secret_word)
            break


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    word = my_word.replace(" ", "")
    if len(word) == len(other_word):
        for i in range(len(word)):
            if word[i] == '_' or word[i] == other_word[i]:
                continue
            else:
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
        if match_with_gaps(my_word, word)== True:
            list_with_words.append(word)
    print(" ".join(list_with_words))


if __name__ == "__main__":
    print("Welcome to the game Hangman!\nDo you want play hangman (classic) or hangman with hints?")
    while type:
        request=input("if you want to play hangman (classic) input 'classic', play hangman with hints input 'hints':")
        if request=="classic" or request=="hints":
            secret_word = choose_word(wordlist)
            hangman(secret_word, request)
            break
        else:
            print("Oops! Your input is not correct")
