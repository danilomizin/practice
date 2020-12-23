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
import string
import re

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, "*": 0
}

WORDLIST_FILENAME = "words.txt"


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
    Returns the score for a word. Assumes the word is a
    valid word.
    """
    count = 0
    for letter in word.lower():
        count += SCRABBLE_LETTER_VALUES[letter]
    return count * max(1, (7 * len(word) - 3 * (n - len(word))))


def display_hand(hand):
    """
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

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    hand["*"] = 1
    for letter in hand:
        if letter in VOWELS and hand[letter] == 1:
            del hand[letter]
            return hand


def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.
    """
    new_hand = hand.copy()
    for letter in word.lower():
        if letter in new_hand and new_hand[letter] > 0:
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
            if letter not in hand or word.count(letter) > hand[letter]:
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
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.
    """
    while calculate_handlen(hand) != 0:
        print("Current Hand:", end=" ")
        display_hand(hand)
        user_word = input("Enter word, or “!!” to indicate that you are finished:")
        if is_valid_word(user_word, hand, word_list):
            count_points += get_word_score(user_word, calculate_handlen(hand))
            print(f"{user_word} earned {str(get_word_score(user_word, calculate_handlen(hand)))} ."
                  f" Total:{count_points} points")
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
    """
    if letter in hand:
        new_hand = hand.copy()
        if letter in VOWELS:
            while True:
                new_letter = random.choice(VOWELS)
                if new_letter not in hand.keys():
                    new_hand[new_letter] = new_hand.pop(letter)
                    return new_hand
        elif letter in CONSONANTS:
            while True:
                new_letter = random.choice(CONSONANTS)
                if new_letter not in hand.keys():
                    new_hand[new_letter] = new_hand.pop(letter)
                    return new_hand
    return hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep
      the better of the two scores for that hand.  This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands
    """
    count_final_points = 0
    number_of_hands = int(input("Enter total number of hands:"))
    while number_of_hands != 0:
        hand = deal_hand(HAND_SIZE)
        print("Current hand:", end=" ")
        display_hand(hand)
        ask_user = str(input("Would you like to substitute a letter?"))
        if ask_user == "yes":
            letter = str(input("Which letter would you like to replace:"))
            hand = substitute_hand(hand, letter)
        print(" ")
        count_of_hand = play_hand(hand, word_list, 0)
        count_final_points += count_of_hand
        print("Total score for this hand:", count_of_hand)
        print("------")
        number_of_hands -= 1

    print("Total score over all hands:", end=" ")
    return count_final_points


if __name__ == '__main__':
    word_list = load_words()
    print(play_game(word_list))
