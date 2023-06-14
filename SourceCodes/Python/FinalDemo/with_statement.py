def with_statement():
    with open('file.txt', 'r') as f:
        read_content = f.read()
    return read_content