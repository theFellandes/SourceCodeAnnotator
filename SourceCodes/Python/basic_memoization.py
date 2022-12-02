from functools import lru_cache

@lru_cache(maxsize=1000)
def fibonacci_memoization(nth_number: int):
    if nth_number < 1:
        return -1

    elif nth_number == 1 or nth_number == 2:
        return 1

    return fibonacci_memoization(nth_number-1) + fibonacci_memoization(nth_number-2)

if __name__ == '__main__':
    print(fibonacci_memoization(4))
