"""
    The Hangman game. Class variables are
    __stages: the hangman stages art
    __wordlist: contains the wordlist
    __guessed_word_list: creates a guessed word list for player
    __game_word: holds the game_word for the player
    __remaining_lives: holds the remaining lives for the player
"""
import random


class Hangman:
    """
    The Hangman game. Class variables are
    __stages: the hangman stages art
    __wordlist: contains the wordlist
    __guessed_word_list: creates a guessed word list for player
    __game_word: holds the game_word for the player
    __remaining_lives: holds the remaining lives for the player
    """

    __stages = [
        """
  +---+
  |   |
      |
      |
      |
      |
=========
""",
        """
  +---+
  |   |
  O   |
      |
      |
      |
=========
""",
        """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
""",
        """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
""",
        """
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
""",
        """
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
""",
        """
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
""",
    ]
    __wordlist = []
    __guessed_word_list = []
    __game_word = []
    remaining_lives = len(__stages)

    def __init__(self, total_lives=len(__stages), wordlist_path=r"wordlist"):
        """
        Constructor is used to read from the wordlist and create the wordlist for the game.
        :argument total_lives: the total lives for the hangman game. Default: 6
        :argument wordlist_path: the path for the wordlist
        """
        # Reading and generating the wordlist
        with open(wordlist_path, "r") as wordlist:
            for word in wordlist:
                word = word[:-1]
                self.__wordlist.append(word)
        # Setting up the game parameters
        self.remaining_lives = total_lives
        self.__game_word = list(random.choice(self.__wordlist))

        for _ in range(len(self.__game_word)):
            self.__guessed_word_list.append("-")

    def hangman(self, guessed_word: str):
        """
        The hangman game logic function.
        It stores the correct_count for detecting the hits on the letter.
        :param guessed_word: the guessed letter from the player
        :return: bool value whether player guessed everything correctly or not
        """
        correct_count = 0
        for i in range(len(self.__game_word)):
            letter = self.__game_word[i]
            if guessed_word.lower() == letter:
                correct_count += 1
                self.__guessed_word_list[i] = letter

        print(self.__guessed_word_list)
        # Returning if letter hits as correct or not.
        return correct_count == 0

    def game_loop(self):
        """
        The game loop for the hangman game.
        :return: void
        """
        print(
            """
         _                                       
        | |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
        | '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
        | | | | (_| | | | | (_| | | | | | | (_| | | | |
        |_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                            __/ |                      
                           |___/
        """
        )
        print("Welcome to the hangman game.")

        # Easter egg value
        same_guessed_number_count = 0
        while self.remaining_lives != 0:
            guessed_word = input("Guess a letter.\n")

            # Removing numeric guesses
            if guessed_word.isnumeric():
                print("This is a number. Guess again.")
                continue

            # Removing non letters
            if not guessed_word.isalpha():
                print("This is not a letter. Guess again.")
                continue

            # Easter egg
            if guessed_word in self.__guessed_word_list:
                print("You already guessed this letter. Guess something else.")
                same_guessed_number_count += 1
                continue

            # Game logic
            is_life_lost = self.hangman(guessed_word=guessed_word.lower())
            self.life_loss(life_loss=is_life_lost)

        if same_guessed_number_count > 10:
            print(
                "What did you expect by guessing the same letter over and over again."
            )
            print(
                f"Congrats you guessed same letter {same_guessed_number_count} times."
            )
        print("Game Over!")
        print("The word was: ")
        answer = ""
        for letter in self.__game_word:
            answer += letter
        print(answer)

    def life_loss(self, life_loss: bool):
        """
        life_loss runs if player loses life and prints out the hangman
        :param life_loss: did player lose life?
        :return:
        """
        if life_loss:
            self.remaining_lives -= 1
            index_of_hangman = len(self.__stages) - self.remaining_lives - 1
            print(self.__stages[index_of_hangman])

    def __debug(self):
        """
        debug method for testing purposes
        :return: void
        """
        print("Psst, the computer picked: ")
        print("###########################")
        print(self.__game_word)
        print("Use this knowledge wisely")
        print("###########################")


def main():
    """
    local main
    :return: void
    """
    hangman = Hangman()
    hangman.game_loop()


if __name__ == "__main__":
    main()
