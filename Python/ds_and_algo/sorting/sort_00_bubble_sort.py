"""Bubble Sort is a simple sorting algorithm that works by repeatedly stepping through the list,
comparing adjacent elements, and swapping them if they're in the wrong order.
This process continues until no more swaps are needed, which means the list is sorted."""


def bubble_sort(arr):
    length = len(arr)

    for i in range(length):
        for j in range(0, length - i - 1):

            print(f"i: {i}, j: {j}  element 1 : {arr[j]}, element 2 : {arr[j + 1]}, arr: {arr}")

            # Swap if the current element is greater than the next
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

    return arr


a = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = bubble_sort(a)
print("Sorted array:", sorted_arr)
