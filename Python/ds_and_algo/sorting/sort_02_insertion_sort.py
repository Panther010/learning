"""Insertion Sort works by building a sorted section of the list,
one element at a time, by inserting each element into its correct position in the sorted section."""


def insertion_sort(arr):
    n = len(arr)

    for i in range(1, n):
        current_value = arr[i]
        position = i
        while position > 0 and arr[position-1] > current_value:
            # print(f"i : {i}, position: {position}, arr: ({arr[position - 1]}, {current_value}) {arr},
            # current_value: {current_value}")
            arr[position] = arr[position-1]
            position -= 1

        arr[position] = current_value
        # print(arr)

    return arr


a = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = insertion_sort(a)
print("Sorted array:", sorted_arr)
