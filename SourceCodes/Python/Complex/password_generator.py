"""
The random password generator for python.
The clean code, SRP rules have been practiced in this file.
The goal of this program is to generate a random password string.

@author: Fellandes
"""
import random
import string


def __main():
    """The private main function for the password_generator"""
    print(
        password_generator(
            password_length=12, include_numbers=True, include_symbols=False
        )
    )


def password_generator(
    password_length: int, include_numbers: bool, include_symbols: bool
):
    """
    The password generator function to randomly generate a string
    :param password_length: the length of the password.
    :param include_numbers: include numbers in the password string or not.
    :param include_symbols: include symbols in the password string or not.
    :return: password string
    """
    # List of ascii letters
    letters = list(string.ascii_lowercase)

    # List of numbers
    if include_numbers:
        numbers = list(range(0, 10))

    # If user doesn't want numbers, include letters
    else:
        numbers = letters

    # List of symbols
    if include_symbols:
        symbols = [
            ",",
            "'",
            "\\",
            "!",
            ".",
            ";",
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
            "=",
            "%",
            "£",
            "#",
            "^",
            "+",
            "/",
            "*",
            "-",
            '"',
            "<",
            ">",
            "&",
            "?",
            "|",
            "_",
            "~",
            "¨",
            "´",
            ":" ";",
            "@",
        ]
    # If user doesn't want symbols, include letters
    else:
        symbols = letters

    # Password string to be printed
    password_string = ""
    for _ in range(0, password_length):
        random_pick = random.randint(0, 2)

        # Pick letter
        if random_pick == 0:
            letter_to_append = random_index_picker(letters)
            password_string += letter_to_append

        # Pick number
        if random_pick == 1:
            number_to_append = random_index_picker(numbers)
            password_string += number_to_append

        # Pick symbol
        if random_pick == 2:
            symbol_to_append = random_index_picker(symbols)
            password_string += symbol_to_append

    return password_string


def random_index_picker(list_of_elements: list):
    """
    random_index_picker picks a random index and returns that random index's
    element with uppercase or lower case
    :param list_of_elements: the list_of_elements to be picked
    :return: element_to_append to the password string
    """
    # random_index = random.randint(0, len(list_of_elements) - 1)
    # element_to_append = random_uppercase_letter(str(list_of_elements[random_index]))
    # return element_to_append
    return random_uppercase_letter(str(random.choice(list_of_elements)))


def random_uppercase_letter(letter: str):
    """
    random_uppercase_letter randomly upper cases a letter or not
    :param letter: letter to be upper cased
    :return: letter: lower case or upper case
    """
    uppercase_or_not = random.randint(0, 1)
    if uppercase_or_not == 1:
        return letter.upper()
    return letter


if __name__ == "__main__":
    __main()
