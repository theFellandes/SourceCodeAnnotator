def try_except():
    try:
        with open('file.txt', 'r') as f:
            f.write('Hello World')
    except IOError:
        raise IOError('File not found')