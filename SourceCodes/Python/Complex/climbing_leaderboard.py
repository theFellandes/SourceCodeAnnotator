def main():
    ranked = [100, 100, 50, 40, 40, 20, 10]
    player = [5, 25, 50, 120]
    climbing_leaderboard(ranked, player)
    ranked2 = [100, 90, 90, 80, 75, 60]
    player2 = [50, 65, 77, 90, 102]
    climbing_leaderboard(ranked2, player2)


def climbing_leaderboard(ranked: list[int], player: list[int]) -> list[int]:
    return [
        int_binary_search(return_sorted_ranked(ranked, rank), rank) + 1
        for rank in player
    ]


def return_sorted_ranked(ranked: list[int], rank: int) -> list[int]:
    """
    Returns the reverse sorted version of the scoreboard
    :param ranked: scoreboard list
    :param rank: player's score
    :return: sorted_rank, the sorted version of the collection
    """
    ranked.append(rank)
    sorted_ranked = list(set(ranked))
    sorted_ranked.sort(reverse=True)
    return sorted_ranked


def int_binary_search(search_array: list[int], value: int) -> int:
    """
    Returns the index of the entered value in search_array
    :param search_array: list of integers
    :param value: desired value searched for index
    :return: index
    """
    low = 0
    high = len(search_array) - 1

    while low <= high:
        mid = (high + low) // 2

        if search_array[mid] < value:
            high = mid - 1

        elif search_array[mid] > value:
            low = mid + 1

        else:
            return mid

    return -1


if __name__ == "__main__":
    main()
