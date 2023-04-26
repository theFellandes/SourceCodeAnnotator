class Foo(object):
    def __init__(self, bruh):
        a = [(1, 2), (3, 4)]
        # Creates a list with elements of a
        # Assigns (<the list of> values 1 to 10 with steps of 2) to x
        x = ((j, i) for i, j in range(1, 10, 2))
        x = [(j, i) for i, j in range(1, 10, 2)]
        x = {i:j for i, j in range(1, 10, 2)}
        # pass
        # Assigns (self.bar, self.x), self.y to (1, 2), 3
        (self.bar, self.x), self.y = (1, 2), 3
        # TODO: Tuple'ları bu şekilde tek parantezli olacak hale getirelim.
        self.bar, self.x, self.y = 1, 2, 3
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
        # for i in a:
            # Iterates over {list_name}
            # print(self.bar)
        for i in self.f():
            # Iterates over {function_name}
            print(i)

    @property
    def bruh2(self):
        f = self.temp
        g = self.temp(1, 2)
        a = {1, 2}
        b = [1, 2]
        f(1, 2)
        return self._bruh + 1

    def f(self):
        return [1, 2, 3, 4, 5]


    @property
    def bruh3(self):
        return 1

    def temp(self, a, b):
        return 'temp'

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
    if num1 > 0 and num1 < 0:
        if num1 > 0:
            if num1 > 0:
                print('a')
        elif num1 < 0:
            if num1 > 0:
                print('a')
        else:
            if num1 > 0:
                print('a')
        print("World")
    else:
        print('c')

if __name__ == "__main__":
    main()