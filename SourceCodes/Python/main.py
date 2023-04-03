class Foo:
    def __init__(self, bruh):
        pass
        # self.bar, self.x = 1, 2
        # self._bruh.bruh += bruh[0]
        # a = 1

    # def get_bar(self):
    #     return self.bar
    #
    # @property
    # def bruh(self):
    #     return self._bruh
    def while_loop(self, a: list):
        # if {subject} matches {case} {do something} or matches {case} {do something}
        match a:
            case [1, 2, 3]:
                print(self.bar)
            case [1, 2, 3, 4, 5]:
                print(self.bar)
            case 1:
                print(self.bar)
            case 2 | 3:
                print(self.bar)

    def while_loop(self, a: list):
        while a:
            print(self.bar)
        while True:
            print(self.bar)


    def for_loop(self, a: list):
        for i in range(1, 10):
            # Iterates over range(10)
            print(i)
        for i in a:
            # Iterates over {list_name}
            print(self.bar)
        for i in self.f():
            # Iterates over {function_name}
            print(i)

    @property
    def bruh2(self):
        f = self.donduranshow
        g = self.donduranshow(1, 2)
        a = {1, 2}
        b = [1, 2]
        f(1, 2)
        return self._bruh + 1

    def f(self):
        return [1, 2, 3, 4, 5]


    @property
    def bruh3(self):
        return 1

    def donduranshow(self, a, b):
        return 'donduranshow'

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