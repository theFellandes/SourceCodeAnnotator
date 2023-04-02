class Foo:
    def __init__(self, bruh):
        self.bar = 1
        self._bruh = bruh

    def get_bar(self):
        return self.bar

    @property
    def bruh(self):
        return self._bruh

    @property
    def bruh2(self):
        return self._bruh + 1

    @property
    def bruh3(self):
        return 1

    @bruh.setter
    def bruh(self, value):
        self._bruh = value

def main():
    num1 = 12
    print_world(num1)
    def inner_function():
        print("Hello")

print("Hello")

def print_world(num1):
    """
    Checks if num1 is greater than 0 and prints world

    @param num1
    @returns void
    """
    if num1 > 0:
        print("World")

if __name__ == "__main__":
    main()