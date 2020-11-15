# Problem Set 2, hangman.py
# Name: Danilo Mizin
# Collaborators: Sofia Piustonen
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random

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

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
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
    counter = 0
    flag = False
    for i in secret_word:
        for f in letters_guessed:
            if i == f:
                flag = True
                break
        if not flag:
            counter += 1
        flag = False
    return counter
    # FILL IN YOUR CODE HERE AND DELETE "pass"



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    s = ""
    for i in range(len(secret_word)):
        if secret_word[i] in letters_guessed:
            s += secret_word[i]
        else:
            s += "_ "

    secret_word = s
    return secret_word

    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    if len(letters_guessed)==0:
        import string
        x = list(string.ascii_lowercase)
        print(''.join(x))
    else:
        import string
        z = list(string.ascii_lowercase)
        for i in letters_guessed:
            del z[z.index(i.lower())]
            y = ''.join(z) # ''
        print(y)
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed=[]
    warnings_point=3
    guesses_point=6
    print("Welcome to the game Hangman!\nI am thinking of a word that is", len(secret_word),"letters long")
    print("You have", warnings_point,"warnings left")
    while guesses_point>0:
        print("-------")
        print("You have", guesses_point, "guesses left")
        print("Available letters:", end=" ")
        get_available_letters(letters_guessed)
        letter=input("Please guess a letter:")
        if str.isalpha(letter.lower())==False or len(letter)!=1:
            warnings_point-=1
            print("Oops! That is not a valid letter or you print more than one letter.",end=" ")
            print("You have", warnings_point, "warnings left:",end=" ")
            print(get_guessed_word(secret_word, letters_guessed))
        elif letter in letters_guessed:
            warnings_point-=1
            print("You have already guessed that letter:",end=" " )
            print("You have", warnings_point,"warnings left:")
            print(get_guessed_word(secret_word, letters_guessed))
            if warnings_point<0:
                guesses_point-=1
                print("Oops! You have no warnings left, so you lose ine guess:",end=' ')
                get_guessed_word(secret_word,letters_guessed)
        else:
            if letter in secret_word:
                letters_guessed.append(letter)
                print("Good guess:", get_guessed_word(secret_word, letters_guessed))
            else:
                letters_guessed.append(letter)
                if letter in "aeoiu":
                    guesses_point-=2
                else:
                    guesses_point-=1
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word,letters_guessed))
        if is_word_guessed(secret_word,letters_guessed)==0:
            final_points=guesses_point*int(len(secret_word))
            print("Congratulations, you won!")
            print("Your total score for this game is:",final_points)
            guesses_point=-1
        if guesses_point==0:
            print("-------")
            print("Sorry, you ran out of guessed. The word was", secret_word)
            break



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word1 = "".join(my_word.split(" "))
    if len(my_word1) == len(other_word):
        for i in range(len(my_word1)):
            if my_word1[i] == '_':
                continue
            elif my_word1[i] == other_word[i]:
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
    final_list = []
    for i in list(wordlist):
        if match_with_gaps(my_word, i) == True:
            final_list.append(i)
        else:
            continue
    if len(final_list) == 0:
        print("No mathces found")
    else:
        return final_list




def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = []
    warnings_point = 3
    guesses_point = 6
    print("Welcome to the game Hangman!\nI am thinking of a word that is", len(secret_word), "letters long")
    print("You have", warnings_point, "warnings left")
    while guesses_point > 0:
        print("-------")
        print("You have", guesses_point, "guesses left")
        print("Available letters:", end=" ")
        get_available_letters(letters_guessed)
        letter = input("Please guess a letter:")
        if letter=="*":
            print("Possible word matches are:", end=" ")
            print(show_possible_matches(get_guessed_word(secret_word,letters_guessed)))
        else:
            if str.isalpha(letter.lower()) == False or len(letter) != 1:
                if warnings_point <= 0:
                    guesses_point -= 1
                    print("Oops! You have no warnings left, so you lose ine guess:", end=' ')
                    get_guessed_word(secret_word, letters_guessed)
                else:
                    warnings_point -= 1
                    print("Oops! That is not a valid letter or you print more than one letter.", end=" ")
                    print("You have", warnings_point, "warnings left:", end=" ")
                    print(get_guessed_word(secret_word, letters_guessed))
            elif letter in letters_guessed:
                if warnings_point <= 0:
                    guesses_point -= 1
                    print("Oops! You have no warnings left, so you lose ine guess:", end=' ')
                    get_guessed_word(secret_word, letters_guessed)
                else:
                    warnings_point -= 1
                    print("You have already guessed that letter:", end=" ")
                    print("You have", warnings_point, "warnings left:")
                    print(get_guessed_word(secret_word, letters_guessed))

            else:
                if letter in secret_word:
                    letters_guessed.append(letter)
                    print("Good guess:", get_guessed_word(secret_word, letters_guessed))
                else:
                    letters_guessed.append(letter)
                    if letter in "aeoiu":
                        guesses_point -= 2
                    else:
                        guesses_point -= 1
                    print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
            if is_word_guessed(secret_word, letters_guessed) == 0:
                final_points = guesses_point * int(len(secret_word))
                print("Congratulations, you won!")
                print("Your total score for this game is:", final_points)
                guesses_point = -1
            if guesses_point == 0:
                print("Sorry, you ran out of guessed. The word was", secret_word)
                break



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
   # secret_word = choose_word(wordlist)
    #print(secret_word)
    #my_word=hangman(secret_word)


###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
