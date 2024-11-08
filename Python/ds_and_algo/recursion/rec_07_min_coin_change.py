def min_coin_required(target, coin_list):

    if target == 0:
        return 0

    if target in coin_list:
        return 1

    else:

        min_coin = target

        for coin in [c for c in coin_list if c <= target]:
            num_coin = 1 + min_coin_required(target - coin, coin_list)

            min_coin = min(min_coin, num_coin)

    return min_coin


print(min_coin_required(63, [1, 5, 10, 25]))
