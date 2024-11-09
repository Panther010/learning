def seq_search(arr, target):
    for index, num1 in enumerate(arr):
        if num1 == target:
            return index

    return -1


def seq_search1(arr, target):
    length = len(arr)
    i = 0
    while i < (length - 1):
        if arr[i] == target:
            return i
        i += 1
    return -1


a = [10, 23, 45, 70, 11, 15]
search = 70
result = seq_search1(a, search)

if result != -1:
    print(f'Element fount in list at index {result}')
else:
    print('Element is not present in the list')
