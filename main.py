import time

from Utils.time_util import get_time


@get_time
def main():
    time.sleep(4)
    print("cu")


if __name__ == '__main__':
    main()
