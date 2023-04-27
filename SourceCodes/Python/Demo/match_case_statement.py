def match_case_with_default(match_value):
    match match_value:
        case 1:
            print('One')
        case 2:
            print('Two')
        case _:
            print('Default')


def match_case_without_default(match_value):
    match match_value:
        case 1:
            print('One')
        case 2:
            print('Two')


if __name__ == '__main__':
    match_case_with_default(1)
