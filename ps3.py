# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Danilo Mizin
# Collaborators :
# Time spent    :

import math
import random
import re

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, "*": 0
}

WORDLIST_FILENAME = "words_ps3.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_word_score(word, n):
    """
    'Word' is word, which user inputted. 'n' is amount letter in 'hand'
    Returns the score for a word. Assumes the word is a
    valid word.
    """
    count = 0
    for letter in word.lower():
        count += SCRABBLE_LETTER_VALUES[letter]
    return count * max(1, (7 * len(word) - 3 * (n - len(word))))


def display_hand(hand):
    """
    'hand' is dictionary with random letters.
    Displays the letters currently in the hand.
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')  # print all on the same line
    print()  # print an empty line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).
    """
    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    hand["*"] = 1
    return hand


def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.
    """
    new_hand = hand.copy()
    for letter in word.lower():
        if letter in new_hand and new_hand.get(letter, 0) > 0:
            new_hand[letter] -= 1
    return new_hand


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    """
    word = word.lower()
    if "*" in word:
        word = word.replace("*", f"[{VOWELS}]")
        for word_g in word_list:
            if re.fullmatch(word, word_g) is not None:
                return True
        else:
            return False
    elif word in word_list:
        for letter in word:
            if letter not in hand or word.count(letter) > hand.get(letter, 0):
                return False
        else:
            return True
    else:
        return False


def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.
    """
    count_letter = 0
    for letter in hand.keys():
        count_letter += hand[letter]
    return count_letter


def play_hand(hand, word_list, count_points):
    """
    The hand finishes when there are no more unused letters.
    The user can also finish playing the hand by inputing two
    exclamation points (the string '!!') instead of a word.
    Returns the number of points, which earned user.
    """
    while calculate_handlen(hand) != 0:
        print("Current Hand:", end=" ")
        display_hand(hand)
        user_word = input("Enter word, or “!!” to indicate that you are finished:")
        if is_valid_word(user_word, hand, word_list):
            score_word = get_word_score(user_word, calculate_handlen(hand))
            count_points += score_word
            print(f"{user_word} earned {str(score_word)}."
                  f" Total: {count_points} points")
            print(" ")
        elif user_word == "!!":
            return count_points
        else:
            print("This is not valid word. Please choose another word")
        hand = update_hand(hand, user_word)
    else:
        return count_points


def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.
    Returns hand, in which was changed selected letter.
    """
    if letter in hand:
        new_hand = hand.copy()
        while True:
            new_letter = random.choice(VOWELS and CONSONANTS)
            if new_letter not in hand:
                new_hand[new_letter] = new_hand.pop(letter)
                return new_hand
    return hand


def ask_user(change_hand, change_letter, string, hand, count_of_hand = 0):
    '''
    'change_hand' is True, if user have shift and False if user can not use shift.
    'string' shows that func need to ask user about change letter or replay hand.
    'hand' is dict with words.
    'count_of_hand' are points for hand.
    User can change letter in word or replay hand. This function ask user, that he/she wants to do
    smt with hand. Then changes letter or replay hand. User can only use one shift.
    Returns points of hand, new 'hand' and change_hand
    '''
    if change_hand:
        if string == "change_letter":
            ask_user = input("Would you like to substitute a letter?")
            if ask_user == "yes":
                letter = input("Which letter would you like to replace:")
                hand = substitute_hand(hand, letter)
                change_letter = False
        elif string == "replay_hand":
            replay_hand = input("Would you like to replay the hand?")
            if replay_hand == "yes":
                count_of_hand = play_hand(hand, word_list, 0)
                print("Total score for this hand:", count_of_hand)
                print("------")
                change_hand = False
    return count_of_hand, hand, change_hand, change_letter


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * Call functions play_hand, it returns a score of hand

    * Returns the total score for the series of hands
    """
    count_final_points = 0
    number_of_hands = int(input("Enter total number of hands:"))
    change_hand = True
    change_letter = True

    while number_of_hands != 0:
        hand = deal_hand(HAND_SIZE)
        print("Current hand:", end=" ")
        display_hand(hand)
        count_of_hand, hand, change_hand, change_letter = \
            ask_user(change_hand, change_letter, 'change_letter', hand)
        print(" ")
        count_of_hand = play_hand(hand, word_list, 0)
        print("Total score for this hand:", count_of_hand)
        print("------")
        count_of_hand, hand, change_hand, change_letter = \
            ask_user(change_hand, change_letter, "replay_hand", hand, count_of_hand)
        count_final_points += count_of_hand
        number_of_hands -= 1

    print("Total score over all hands:", end=" ")
    return count_final_points


if __name__ == '__main__':
    word_list = load_words()
    print(play_game(word_list))
