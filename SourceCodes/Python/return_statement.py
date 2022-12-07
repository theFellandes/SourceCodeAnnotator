import random


def main():
    random_number = get_random_number(0, 10)
    random_number2 = get_random_number(0, 10)
    random_numbers_added = addition(random_number, random_number2)
    user_id = increment_number_by_one(get_default_user_id())
    user_id = increment_number_by_20(user_id)
    stanza = append_string_with_stanza("Stanza")

def get_random_number(lower_bound: int, upper_bound: int) -> int:
    return random.randint(lower_bound, upper_bound)

def addition(number1: int, number2: int):
    return number1 + number2

def get_default_user_id():
    return 20

def increment_number_by_one(number: int):
    number += 1
    return number

def increment_number_by_20(number: int):
    return number + 20

def append_string_with_stanza(input_string: str):
    return input_string + " Stanza"


if __name__ == '__main__':
    main()
