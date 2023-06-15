def write_to_file(path, message):
    with open(path, 'w') as file:
        file.write(message)


def main():
    user_input = input('Enter a message: ')
    if len(user_input) > 80:
        raise ValueError('Message is too long')

    else:
        write_to_file('file.txt', user_input)
        print('Message written to file')


def encrypt_message(message, key):
    encrypted_message = ""
    for char in message:
        encrypted_char = chr(ord(char) + key)
        encrypted_message += encrypted_char
    return encrypted_message


def draw_circle(radius):
    pygame.init()

    width = 800
    height = 600
    screen = display.set_mode((width, height))
    display.set_caption("Circle")

    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)

    screen.fill(BLACK)
    circle_center = (width // 2, height // 2)
    draw_circle(screen, BLUE, circle_center, radius)

    display.show()
    pygame.quit()


def check_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True


def find_max(numbers):
    if len(numbers) == 0:
        return None
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num
