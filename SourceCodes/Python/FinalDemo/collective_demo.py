def write_to_file(path, message):
    with open(path, 'w') as f:
        f.write(message)


def main():
    user_input = input('Enter a message: ')
    if len(user_input) > 80:
        raise ValueError('Message is too long')

    else:
        write_to_file('file.txt', user_input)
        print('Message written to file')
