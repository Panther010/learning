def cumulative_sum(n):

    # base case
    if n == 0:
        return 0
    else:
        return n + cumulative_sum(n-1)


print(cumulative_sum(9))
