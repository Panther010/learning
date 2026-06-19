# Find duplicates in a list data = [1, 3, 4, 2, 2, 3, 5, 6, 6, 7] # Expected output: [2, 3, 6]
data1 = [1, 3, 4, 2, 2, 3, 5, 6, 6, 7]
def duplicate_finder(data: list) -> list:
    frequency_map = {}
    duplicates = []
    if len(data) <= 1:
        return []

    for value in data:
        frequency_map[value] = frequency_map.get(value, 0) + 1

    for value, count in frequency_map.items():
        if count > 1:
            duplicates.append(value)

    return duplicates
print(duplicate_finder(data1))


# Flatten a nested list data = [[1, 2, 3], [4, 5], [6, 7, 8, 9], [10]] # Expected output: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
def list_flattener(arr: list) -> list:
    return [item for sublist in arr for item in sublist]

print(list_flattener([[1, 2, 3], [4, 5], [6, 7, 8, 9], [10]]))


# Group words by their first letter words = ["apple", "avocado", "banana", "blueberry", "cherry", "apricot", "cranberry"]
# Expected output: {'a': ['apple', 'avocado', 'apricot'], 'b': ['banana', 'blueberry'], 'c': ['cherry', 'cranberry']}

def group_words(words: list) -> dict:
    words_map = {}

    for word in words:
        words_map.setdefault(word[0], []).append(word)
    return words_map

print(group_words(["apple", "avocado", "banana", "blueberry", "cherry", "apricot", "cranberry"]))


# Rotate a list by k positions data = [1, 2, 3, 4, 5, 6, 7] # k = 3 # Expected output: [5, 6, 7, 1, 2, 3, 4]
def rotate_list(arr:list, rotator: int) -> list:
    if not arr:
        return []

    rotator = rotator % len(arr)
    result = arr[-rotator:] + arr[:-rotator]

    return result

print(rotate_list([1, 2, 3, 4, 5, 6, 7], 3))


# Find the two numbers that sum to a target (Two Sum) numbers = [2, 7, 11, 15, 1, 8, 3] # target = 9
def target_sum(arr: list, target: int) -> list:
    result = []
    seen = set()

    for num in arr:
        if target - num in seen:
            result.append((min(num, target -num), max(num, target - num)))
        else:
            seen.add(num)

    return result

print(target_sum([2, 7, 11, 15, 1, 8, 3], 9))


# Parse and aggregate a log file
ogs = [
 "2026-06-01 ERROR database connection failed",
 "2026-06-01 INFO pipeline started",
 "2026-06-02 WARNING memory usage high",
 "2026-06-02 ERROR timeout on job 42",
 "2026-06-03 INFO pipeline completed",
 "2026-06-03 ERROR disk full",
]
# Task: Return a dict with count of each log level
# Expected output: {'ERROR': 3, 'INFO': 2, 'WARNING': 1}
def parser(logs: list) -> dict:
    result = {}
    for rows in logs:
        data = rows.split()
        log_date = data[0]
        log_type = data[1]
        log_location = data[2]
        result[log_type] = result.get(log_type, 0) + 1
    return result

print(parser(ogs))

