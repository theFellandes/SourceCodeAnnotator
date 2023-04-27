def operations_with_long_string():
    a_really_long_string = 'This is a' + 'Really, really long' + 'string' + 'you can believe us.' + 'it is really long'
    a_really_long_string *= 2

    num1 = 1
    num2 = 2
    num3 = num1 + num2
    num3 += num1

def operations_with_numbers(num1, num2):
    num1 **= num2
    return num1


if __name__ == '__main__':
    operations_with_long_string()
    operations_with_numbers(1, 2)