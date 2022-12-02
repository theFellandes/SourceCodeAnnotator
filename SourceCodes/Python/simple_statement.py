def main():
    simple_if_statement()
    simple_for_loop()
    simple_if_with_parameter(2+2)

def simple_if_statement():
    if 3 < 5:
        print("3 is less than 5")

    elif 3 == 5:
        print("3 is equal to 5")

    else:
        print("wtf")

def simple_for_loop():
    for i in range(0, 10):
        print("looping")

def simple_if_with_parameter(comparison_item):
    if comparison_item < 5:
        print(f"{comparison_item} is less than 5")

    elif comparison_item == 5:
        print(f"{comparison_item} equals to 5")

    else:
        print(f"{comparison_item} is greater than 5")


if __name__ == '__main__':
    main()