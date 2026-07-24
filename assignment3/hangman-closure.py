# Task 4: Closure Practice

def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter)

        display_word = ""

        for character in secret_word:
            if character in guesses:
                display_word += character
            else:
                display_word += "_"

        print(display_word)

        if "_" in display_word:
            return False
        else:
            return True

    return hangman_closure


secret_word = input("Enter the secret word: ")
game = make_hangman(secret_word)

finished = False

while not finished:
    guess = input("Guess a letter: ")
    finished = game(guess)

print("You guessed the word!")