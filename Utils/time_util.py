from functools import wraps
from time import perf_counter


def get_time(func):
    """ Finds total execution time of a function """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()

        return_value = func(*args, **kwargs)

        end_time = perf_counter()
        total_time = round(end_time - start_time, 4)

        print(f'Time: {total_time} seconds')

        return return_value
    return wrapper
