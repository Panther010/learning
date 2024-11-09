"""Selection Sort is a simple sorting algorithm that works by dividing the list into a sorted and unsorted section.
It repeatedly finds the minimum element from the unsorted section and moves it to the end of the sorted section."""


def selection_sort(arr):
    n = len(arr)

    for i in range(n):
        min_index = i  # assume first/ current number is the smallest number

        for j in range(i+1, n):  # Find the minimum element in the remaining unsorted section
            if arr[j] < arr[min_index]:
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i]  # Swap the found minimum element with the first element

    return arr


def selection_sort1(arr):
    n = len(arr)

    for i in range(n):
        max_index = 0
        for j in range(1, n - i):

            if arr[j] > arr[max_index]:
                max_index = j

        arr[n-i-1], arr[max_index] = arr[max_index], arr[n-i-1]

    return arr


a = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = selection_sort(a)
print("Sorted array:", sorted_arr)
