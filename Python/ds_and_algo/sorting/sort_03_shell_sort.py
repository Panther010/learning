def shell_sort(arr):
    sublist_counter = len(arr) // 2

    while sublist_counter > 0:
        for start in range(sublist_counter):
            gap_insertion_sort(arr, start, sublist_counter)

        print(f"sublist_counter: {sublist_counter}, arr: {arr}")
        sublist_counter = sublist_counter // 2

    return arr


def gap_insertion_sort(arr, start, gap):

    for i in range(start+gap, len(arr), gap):
        current_value = arr[i]
        position = i

        while position >= gap and arr[position - gap] > current_value:
            print(f"i : {i}, position: {position}, arr: ({arr[position - gap]}, {current_value}) {arr}, current_value: {current_value}")
            arr[position] = arr[position - gap]

            position -= gap

        arr[position] = current_value


a = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = shell_sort(a)
print("Sorted array:", sorted_arr)
