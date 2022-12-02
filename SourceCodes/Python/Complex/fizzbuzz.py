"""

This python file is an exercise python code for clean coding and commenting.
The main purpose for the codes are to test pylint.
This python file includes a clean code style written fizz_buzz game.
Written by: Fellandes

"""


def __main():

    """
     Private main method for testing fizzbuzz.
    :return: void
    """
    fizz_buzz_print(1, 101)


def fizz_buzz(number: int):

    """
    Takes in a number number, finds if it can divide by 3 or 5.
    If the number can divide by 3, appends output_word with Fizz.
    If the number can divide by 5, appends output_word with Buzz.
    If the number can divide by 15, creates output_word as FizzBuzz.
    If it cannot divide by 3 and 5, the output_word will be filled with original number.
    :argument number = input value to be tested.
    :return string fizz_buzz value
    """

    output_word = ""

    if number % 3 == 0:
        output_word += "Fizz"

    if number % 5 == 0:
        output_word += "Buzz"

    if output_word == "":
        output_word = str(number)

    return output_word


def fizz_buzz_print(sequence_start: int, sequence_end: int):

    """
    Prints the fizz_buzz for the start value and end value.
    sequence_start = the start value for the fizz_buzz game.
    sequence_end = the end value for the fizz_buzz game.
    :argument sequence_start = sequence start value for the fizz_buzz
    :argument sequence_end = sequence end value for the fizz_buzz
    :return void
    """

    for number in range(sequence_start, sequence_end):
        fizz_buzz_value_for_number = fizz_buzz(number)
        print(fizz_buzz_value_for_number)


if __name__ == "__main__":
    __main()
