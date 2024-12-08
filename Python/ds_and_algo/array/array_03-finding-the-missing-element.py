import collections
import re


def finder1(arr1, arr2):
    arr1.sort()
    arr2.sort()

    for num1, num2 in zip(arr1, arr2):
        if num1 != num2:
            return num1

    return arr1[-1]


def finder2(arr1, arr2):
    count = collections.defaultdict(int)

    for num2 in arr2:
        count[num2] += 1

    for num1 in arr1:

        if count[num1] == 0:
            return num1
        else:
            count[num1] -= 1
        print(count)


def finder3(arr1, arr2):
    return sum(arr1) - sum(arr2)


def finder(arr1, arr2):
    res = 0
    for num1 in arr1 + arr2:
        res ^= num1
        print(res)

    return res


a1 = [1, 2, 3, 4, 5, 6, 7]
a2 = [3, 7, 2, 1, 4, 6]
print(finder(a1, a2))
