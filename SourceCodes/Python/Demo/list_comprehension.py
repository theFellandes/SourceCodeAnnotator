def list_comprehension():
    x = [i for i in range(10)]
    y = (i for i in range(10))
    z = {i for i in range(10)}
    t = {i: i for i in range(10)}
    x += y
    t **= z
    return x, y, z, t


if __name__ == '__main__':
    list_comprehension()
