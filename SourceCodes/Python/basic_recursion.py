def main():
    fibonacci(2)

def fibonacci(nth_number):
    if nth_number <= 1:
        return nth_number
    return fibonacci(nth_number - 1) + fibonacci(nth_number - 2)