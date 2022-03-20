"""
This program helps users find answers for the Wordle game
based on what they guessed and the green, yellow, black (grey) results they got.

Author: Woramon P.
Date: 3/20/22
"""

import string
from word_list import ALL_WORDS


def new_game():
    all_words = ALL_WORDS
    word_length = 5
    must_have_letters = set()  # letters that are known to be green or yellow
    possible_indexes = {s: set(range(word_length)) for s in string.ascii_uppercase}
    # a dict of possible indexes for each letter
    # all letters start off as possible in all positions
    # i.e. {'A': {0, 1, 2, 3, 4}, 'B': {0, 1, 2, 3, 4} ..... 'Z': {0, 1, 2, 3, 4}}
    known_green_letters = {s: set() for s in string.ascii_uppercase}

    while True:  # keep trying until we get the final answer

        # get input
        while True:  # keep asking to enter a word until the word is valid
            input_word = input("\nEnter the word you guessed.\n>> ").upper()
            if len(input_word) == word_length and input_word.isalpha():

                while True:  # keep asking to enter the result until the result is valid
                    input_result = input(f"Enter the color result for {input_word}.\n>> ").upper()
                    if input_result == 'G' * word_length:
                        # meaning that users got all the letters right
                        print("Congrats!")
                        return
                    elif len(input_result) == word_length and all(x in 'GYB' for x in input_result):
                        # acceptable input format
                        break
                    else:
                        print(f"Please use only the letters G, Y, B, and make sure you only type {word_length} of them.")

                # check if entered result conflicts with previous info
                green_letters = []
                yellow_letters = []
                black_letters = []
                valid_input = True

                for index, r in enumerate(input_result):
                    to_append = (index, input_word[index])
                    if r == 'G':
                        green_letters.append(to_append)
                    elif r == 'Y':
                        yellow_letters.append(to_append)
                    else:
                        black_letters.append(to_append)

                for index, letter in green_letters:
                    if index not in possible_indexes[letter]:
                        valid_input = False
                        print(f"* Check position {index + 1}: {letter} can't be green here.")
                for index, letter in yellow_letters + black_letters:
                    if index in known_green_letters[letter]:
                        valid_input = False
                        print(f"* Check position {index + 1}: You stated that {letter} is green.")

                if not valid_input:
                    continue  # if input is invalid, then ask for the word and result again
                else:
                    # if input is valid, then deal with possible_indexes based on info we have

                    for index, letter in green_letters:
                        for letter_in_dict, indexes in possible_indexes.items():
                            indexes.discard(index)
                            # because only one letter can occupy each green position
                            # we remove the index number (i.e. that position) from all letters
                            # and in the next step, we add that position back only to the correct letter
                        possible_indexes[letter].add(index)
                        known_green_letters[letter].add(index)
                        must_have_letters.add(letter)

                    for index, letter in yellow_letters:
                        possible_indexes[letter].discard(index)
                        # if it's yellow, this index position can't be right
                        must_have_letters.add(letter)

                    for index, letter in black_letters:
                        if letter not in [char for ind, char in green_letters + yellow_letters]:
                            # e.g. user guessed AABBB and both As are black
                            # if there is no green or yellow A in this guess, only the black A(s)
                            # then A can't be right in any positions
                            possible_indexes[letter].clear()
                        elif letter in [char for ind, char in green_letters] and letter not in [char for ind, char in yellow_letters]:
                            # e.g. user guessed BAAAB and the first two As are green, the third A is black
                            # no yellow A
                            # then A can't be in any positions except the ones in green
                            # so we will remove all index positions from A first and add back only the green ones
                            possible_indexes[letter].clear()
                            for ind, char in green_letters:
                                if char == letter:
                                    possible_indexes[letter].add(ind)
                        elif letter in [char for ind, char in yellow_letters]:
                            # e.g. user guessed BAAAB and the first two As are yellow, the third A is black
                            # there may or may not be a green A in this guess
                            possible_indexes[letter].discard(index)

                    break  # done with processing entered word

            else:
                print(f"Please enter a {word_length}-letter combination.")
                continue

        # check each word to see if it matches with possible_indexes info we have
        possible_words = []
        for word in all_words:
            if any(letter not in word for letter in must_have_letters):
                # if any of the must-have letters aren't present, then this can't be the right word
                continue
            else:
                for index, letter in enumerate(word):
                    if index not in possible_indexes[letter]:
                        # if a letter appears in an index that was eliminated, then this can't be the right word
                        break
                else:
                    # if the for loop above completes without breaking
                    # i.e. every letter in this word fits with the possible indexes
                    possible_words.append(word)

        # display results
        if len(possible_words) == 0:
            print("\nSorry, I can't find any word based on the clues.")
            return
        elif len(possible_words) == 1:
            print("\nThe answer is", possible_words[0])
            return
        else:
            print("\nYour choices:", ", ".join(possible_words))
            all_words = possible_words  # reduce the list of words, help with the next check


if __name__ == "__main__":
    print("""
Welcome to the Wordle Helper! I'll help you find potential answers based on the clues you have.
Just tell me the word you guessed in Wordle, and the color result you got.
For the color result, type G for Green, Y for Yellow, B for Black/Grey. 
For example, if the color result is Green Green Black Yellow Black, then type GGBYB to me.
The first guess is up to you, so go ahead and try any word in Wordle, then let me know the colors you get.""")
    new_game()
    while True:
        if 'Y' == input("\nType Y and I'll help you with a new word.\n>> ").upper():
            new_game()
        else:
            print("Have a great day. Bye!")
            break
