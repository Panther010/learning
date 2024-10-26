def digit_sum(num1):

    # base case
    if num1 < 10:
        return num1
    else:
        return (num1 % 10) + digit_sum(num1 // 10)


print(digit_sum(9876))
