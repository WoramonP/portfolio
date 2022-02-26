"""
Wordle: Guess a five-letter word. Original game at https://www.nytimes.com/games/wordle/index.html
In the original game, guesses must be real words.
In this game, I added an easy mode option, in which guesses can be non-words.
Author: Woramon P.
Date: 2/18/22
"""

from random import choice
from colorama import Back, Style

# game setup: get words and define parameters
potential_answers = []
with open("Wordle_potential_answers.txt") as f:
    for line in f:
        potential_answers.append(line.strip())

allowed_words = []
with open("Wordle_allowed.txt") as f:
    for line in f:
        allowed_words.append(line.strip())

word_length = 5
max_attempt = 6

# instruction and choosing play mode
print(f"""\nGuess the word in {max_attempt} tries. Each guess must be {word_length} letters. 
After each guess, the color will show how close your guess was to the word.""")
print(Back.GREEN + "Green:", Style.RESET_ALL + "The letter is in the word and in the correct spot.")
print(Back.YELLOW + "Yellow:", Style.RESET_ALL + "The letter is in the word but in the wrong spot.")
print(Back.BLACK + "Black:", Style.RESET_ALL + "The letter is not in the word in any spot.\n")

print(f"""Play mode options
Easy: Guesses can be any {word_length}-letter combinations, e.g. 'HAPPY', 'AEIOU', 'AAAAA'
Normal: Guesses must be real words\n""")

while True:
    play_mode = input("Which mode do you want to play? 'e' for easy, 'n' for normal.\n>> ").lower()
    if play_mode in ['e', 'n']:
        break

# keeps playing until player chooses to exit
while True:

    target = choice(potential_answers).upper()

    letters_green_or_yellow = set()  # letters that are known to be present in target word
    letters_banned = set()  # letters that are guessed, but not in green or yellow
    # therefore, player knows that these letters aren't present in the answer
    all_attempt_results = []  # keep track of results to print
    attempt_count = 0

    for attempt in range(max_attempt):  # each iteration represents one attempt
        attempt_count += 1
        index_green = []  # index of letters that are correct
        index_yellow = []  # index of letters that are present but in an incorrect position
        index_to_be_checked = [True] * word_length
        # True, meaning the guessed letter at this index position still needs to be checked

        target_letters = list(target)

        # get input and check if it's valid
        while True:
            guess = input(f"Attempt #{attempt_count}. Enter your word: ").upper()
            if len(guess) == word_length and guess.isalpha():
                letters_banned_but_used = {letter for letter in guess if letter in letters_banned}
                if len(letters_banned_but_used) == 0:
                    if play_mode == 'n' and guess not in allowed_words:
                        print("Sorry. Not a recognized word.")
                    else:
                        break
                elif len(letters_banned_but_used) == 1:
                    print(f"Can't contain letter {''.join(letters_banned_but_used)}. \
You know it's not in the answer.")
                else:  # len(letters_banned_but_used) > 1
                    print(f"Can't contain letters {', '.join(letters_banned_but_used)}. \
You know they're not in the answer.")
            else:
                print(f"Please enter a {word_length}-letter combination.")

        # check for green: letters that are correct
        for index in range(word_length):
            if guess[index] == target[index]:
                letters_green_or_yellow.add(guess[index])
                index_green.append(index)
                index_to_be_checked[index] = False  # if False, this position won't be checked again this attempt
                target_letters[index] = ""  # if blank, this letter won't be matched again this attempt

        # check for yellow: letters that are present but in an incorrect position
        for index in range(word_length):
            if index_to_be_checked[index]:
                if guess[index] in target_letters:
                    letters_green_or_yellow.add(guess[index])
                    index_yellow.append(index)
                    index_to_be_checked[index] = False
                    target_index = target_letters.index(guess[index])  # where is this letter in the target word?
                    target_letters[target_index] = ""

        # add incorrect letters to the set of banned letters
        index_black = [index for index in range(word_length) if index_to_be_checked[index]]
        for index in index_black:
            if guess[index] not in letters_green_or_yellow:
                letters_banned.add(guess[index])

        # keep track of results; each tuple contains a guessed letter and its background color
        this_attempt_result = []
        for index in range(word_length):
            if index in index_green:
                this_attempt_result.append(tuple((guess[index], "green")))
            elif index in index_yellow:
                this_attempt_result.append(tuple((guess[index], "yellow")))
            else:
                this_attempt_result.append(tuple((guess[index], "black")))

        all_attempt_results.append(this_attempt_result)

        # print results with color clues
        for each_attempt in all_attempt_results:  # get a list for each attempt
            for letter, color in each_attempt:  # get a tuple for each letter & its color
                if color == "green":
                    print(Back.GREEN + letter, end="")
                elif color == "yellow":
                    print(Back.YELLOW + letter, end="")
                else:
                    print(Back.BLACK + letter, end="")
            print(Style.RESET_ALL)  # reset the style, plus get a new line

        # check game end
        if len(index_green) == word_length:
            print(f"Congrats! You win in {attempt_count} attempt(s)!")
            break
        elif attempt_count == max_attempt:
            print(f"Oh no! The correct answer is {target}.")

    play_mode = input("\nPlay again? \
Enter 'e' for easy mode, 'n' for normal mode, other keys to exit.\n>> ").lower()
    if play_mode in ['e', 'n']:
        continue
    else:
        print("Thank you for playing. Have a nice day!")
        break
