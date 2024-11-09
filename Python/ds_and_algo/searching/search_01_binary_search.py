def bin_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        print(f'left : {left}, right: {right}, mid : {mid}, target: {target}, number : {arr[mid]}')

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = left - 1
    return -1


def bin_search_rec(arr, target, left=0, right=None):
    if right is None:
        right = len(arr) - 1

    if left > right:
        return -1

    mid = (left + right) // 2

    print(f'left : {left}, right: {right}, mid : {mid}, target: {target}, number : {arr[mid]}')

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return bin_search_rec(arr, target, mid + 1, right)
    else:
        return bin_search_rec(arr, target, left, mid - 1)


a = [1, 3, 5, 7, 9, 11, 13, 15]
search = 13
result = bin_search_rec(a, search)

if result != -1:
    print(f'Element fount in list at index {result}')
else:
    print('Element is not present in the list')
