"""Test code for sliding window algorithm"""
import random


def main():
    """Main method for sliding window algorithm"""
    numbers_list = [random.randint(0, 100) for _ in range(10)]
    consecutive_elements = random.randint(1, 9)

    # Testing function
    hypothesis = sliding_window_max_sum(numbers_list=numbers_list,
                                        consecutive_elements=consecutive_elements)
    print(numbers_list, consecutive_elements)
    print(hypothesis)

    # Testing error
    sliding_window_max_sum([], 10)


def sliding_window_max_sum(numbers_list: list, consecutive_elements: int) -> int:
    """
    Return the maximum sum of given consecutive elements

    Keyword Arguments:
        :return: sum of consecutive elements
        :rtype: int
        :argument numbers_list: list of numbers
        :argument consecutive_elements: the number
            of consecutive elements to be summed.
    """
    numbers_list_size = len(numbers_list)

    # Checks if invalid consecutive element size
    if numbers_list_size <= consecutive_elements:
        raise IndexError("Invalid sliding window size")

    # Finds window sum for first consecutive element group
    window_sum = 0
    for i in range(consecutive_elements):
        window_sum += numbers_list[i]
    max_sum = window_sum

    for i in range(numbers_list_size - consecutive_elements):
        window_sum = window_sum - numbers_list[i] \
                     + numbers_list[i + consecutive_elements]
        max_sum = max(window_sum, max_sum)

    return max_sum


if __name__ == '__main__':
    main()
