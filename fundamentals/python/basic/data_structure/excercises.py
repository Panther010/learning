"""
Sum of List Elements
Write a Python function that calculates the sum of all elements in a given list of integers.

Parameters:
numbers (List of integers): The input list containing integers.

Returns:
An integer representing the sum of all elements in the input list.

Example:
Input: numbers = [1, 2, 3, 4, 5]
Output: 15
Input: numbers = [10, -5, 7, 8, -2]
Output: 18
"""
def sum_list(numbers):
    # Your code goes here
    result = 0
    for i in numbers:
        result += i

    return result

"""
Largest Element in a List
Find the Largest Element in a List

Write a Python function that finds and returns the largest element in a given list of integers.
Parameters:
numbers (List of integers): The input list containing integers.

Returns:
An integer representing the largest element in the input list.

Example:
Input: numbers = [3, 8, 2, 10, 5]
Output: 10
Input: numbers = [-5, -10, -2, -1, -7]
Output: -1
"""
def find_largest(numbers):
    largest = numbers[0]
    for n in numbers[1:]:
        if n > largest:
            largest = n
    return largest


"""
Remove Duplicates from a List
You are given a list of integers. Write a Python program that removes any duplicate elements from the list and returns a new list with only unique elements. The order of elements in the list should be maintained.

Parameters:
lst (List of integers): The list of integers from which duplicates should be removed.

Returns:
A list of integers where all duplicates have been removed, preserving the original order.

Example:

Input: lst = [1, 2, 2, 3, 4, 4, 5]
Output: [1, 2, 3, 4, 5]
Input: lst = [4, 5, 5, 4, 6, 7]
Output: [4, 5, 6, 7]
"""
def remove_duplicates(lst):
    result = []

    for n in lst:
        if n not in result:
            result.append(n)

    return result

def remove_duplicates1(lst):
    result = []
    seen = set()
    for n in lst:
        if n not in seen:
            result.append(n)
            seen.add(n)
    return result


"""
Check if All Elements in a List are Unique
You are given a list of integers. Write a Python program that checks if all elements in the list are unique. If all elements are unique, return True; otherwise, return False.

Parameters:
lst (List of integers): The list of integers to check for uniqueness.

Returns:
A boolean value True if all elements in the list are unique, False otherwise.

Example:
Input: lst = [1, 2, 3, 4, 5]
Output: True
Input: lst = [1, 2, 3, 3, 4, 5]
Output: False
"""

def check_unique(lst):
    seen = set()
    if len(lst) <= 1:
        return True
    for n in lst:
        if n in seen:
            return False
        else:
            seen.add(n)

    return True


"""
Reverse a List (Non-Slicing Approach)
You are given a list of integers. Write a Python program that reverses the list without using slicing (lst[::-1]). The program should return the reversed list.

Parameters:
lst (List of integers): The list of integers to be reversed.

Returns:
A list of integers where the order of elements is reversed from the input list.

Example:
Input: lst = [1, 2, 3, 4, 5]
Output: [5, 4, 3, 2, 1]
"""
def reverse_list(lst):
    result = []
    for i in range(len(lst)-1, -1, -1):
        result.append(lst[i])

    return result


"""
Count Even and Odd Numbers in a List
You are given a list of integers. Write a Python program that counts and returns the number of even and odd numbers in the list.

Parameters:
lst (List of integers): The list of integers where you will count the even and odd numbers.

Returns:
A tuple (even_count, odd_count) where even_count is the number of even numbers and odd_count is the number of odd numbers.

Example:
Input: lst = [1, 2, 3, 4, 5]
Output: (2, 3)

There are 2 even numbers: 2, 4
There are 3 odd numbers: 1, 3, 5
"""
def count_even_odd(lst):
    odd_counter = 0
    even_counter = 0
    for n in lst:
        if n %2 == 0:
            even_counter += 1
        else:
            odd_counter += 1
    return even_counter, odd_counter


"""
Find Maximum Difference Between Two Consecutive Elements (Brute Force Approach)
You are given a list of integers. Write a Python program to find the maximum difference between two consecutive elements in the list using a brute-force approach. The difference is defined as the absolute value of the difference between two consecutive elements.

Parameters:
lst (List of integers): A list of integers.

Returns:
An integer representing the maximum difference between two consecutive elements.

Example:
Input: lst = [1, 7, 3, 10, 5]
Output: 7
The maximum difference is between 3 and 10 (i.e., |3 - 10| = 7).
Input: lst = [10, 11, 15, 3]
Output: 12
The maximum difference is between 15 and 3 (i.e., |15 - 3| = 12).
"""
def max_consecutive_difference(lst):
    if len(lst) <= 1:
        return 0
    prev = lst[0]
    result = 0
    for n in lst[1:]:
        if abs(n -prev) > result:
            result = abs(n - prev)
        prev = n

    return result


"""
Merge Two Sorted Lists
You are given two sorted lists of integers. Write a Python function to merge these two sorted lists into one sorted list. The resulting list should also be in non-decreasing order.

Parameters:
list1 (List of integers): The first sorted list.
list2 (List of integers): The second sorted list.

Returns:
A single list of integers, containing all elements from list1 and list2, sorted in non-decreasing order.

Example:
Input: list1 = [1, 3, 5], list2 = [2, 4, 6]
Output: [1, 2, 3, 4, 5, 6]
Input: list1 = [1, 4, 7], list2 = [2, 3, 5, 8]
Output: [1, 2, 3, 4, 5, 7, 8]
"""

def merge_two_sorted_lists(list1, list2):
    i = j = 0
    result = []

    while i<len(list1) and j<len(list2):
         if list1[i] <= list2[j]:
             result.append(list1[i])
             i += 1
         else:
             result.append(list2[j])
             j += 1

    while i<len(list1):
        result.append(list1[i])
        i += 1

    while j<len(list2):
        result.append(list2[j])
        j += 1

    return result

print(merge_two_sorted_lists([1, 3, 5], [2, 4, 6]))
print(merge_two_sorted_lists([1, 4, 7], [2, 3, 5, 8]))


"""
Rotate a List (Without Slicing)
You are given a list of integers and an integer k. Write a Python function to rotate the list to the right by k positions without using slicing. A rotation shifts elements from the end of the list to the front.

Parameters:
lst (List of integers): The list to be rotated.

k (Integer): The number of positions to rotate the list.
Returns:

A list of integers rotated by k positions.
Example:

Input: lst = [1, 2, 3, 4, 5], k = 2
Output: [4, 5, 1, 2, 3]
Input: lst = [10, 20, 30, 40, 50], k = 3
Output: [30, 40, 50, 10, 20]
"""
def rotate_list_new(lst, k):
    length = len(lst)

    if length == 0:
        return []

    k = k % length
    result = [0] * length

    for i in range(length):
        new_index = (i+length+k) % length
        result[new_index] = lst[i]

    return result

def rotate_list_new1(lst, k):
    length = len(lst)

    if not lst:
        return []

    k = k % length

    for i in range(k):
        last_element = lst.pop()
        lst.insert(0, last_element)

    return lst

print(rotate_list_new1([1, 2, 3, 4, 5], 3))
print(rotate_list_new1([1, 2, 3, 4, 5], 2))
print(rotate_list_new1([], 2))


"""
Merge Lists to Dictionary
Design a Python function named merge_lists_to_dictionary to merge two lists into a dictionary where elements from the first list act as keys and elements from the second list act as values.

Parameters:
keys (List): A list of keys.
values (List): A list of values.

Returns:
A dictionary containing merged key-value pairs.

Example:

Input: keys = ['a', 'b', 'c'], values = [1, 2, 3]
Output: {'a': 1, 'b': 2, 'c': 3}
Input: keys = ['x', 'y', 'z'], values = [10, 20, 30]
Output: {'x': 10, 'y': 20, 'z': 30}

"""
def merge_lists_to_dictionary(keys, values):
    if len(keys) != len(values):
        return False

    result = {}
    for key, val in zip(keys, values):
        result[key] = val
    return result

print(merge_lists_to_dictionary(['a', 'b', 'c'], [1, 2, 3]))
print(merge_lists_to_dictionary(['x', 'y', 'z'], [10, 20, 30]))
print(merge_lists_to_dictionary(['key1', 'key2'], [100]))



"""
Merge Three Dictionaries
Design a Python function named merge_three_dictionaries to merge exactly three dictionaries into one.

Parameters:
dict1 (Dictionary): The first dictionary to be merged.
dict2 (Dictionary): The second dictionary to be merged.
dict3 (Dictionary): The third dictionary to be merged.

Returns:
A single dictionary containing all key-value pairs from the three input dictionaries.
Example:
Input: ({'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 5, 'f': 6})
Output: {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
Input: ({'x': 10, 'y': 20}, {'z': 30}, {'a': 40, 'b': 50})
Output: {'x': 10, 'y': 20, 'z': 30, 'a': 40, 'b': 50}
"""
def merge_three_dictionaries(dict1, dict2, dict3):
    result = {}

    for d in (dict1, dict2, dict3):
        for key, value in d.items():
            result[key] =value
    return result


print(merge_three_dictionaries({'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 5, 'f': 6}))


"""
Count Word Frequency
Design a Python function named count_word_frequency to count the frequency of words in a sentence and store the counts in a dictionary.

Parameters:
sentence (str): The input sentence where you need to count the frequency of each word.

Returns:
A dictionary where the keys are words from the sentence and the values are their corresponding frequencies.

Example:
Input: "hello world hello"
Output: {'hello': 2, 'world': 1}
Input: "the quick brown fox jumps over the lazy dog"
Output: {'the': 2, 'quick': 1, 'brown': 1, 'fox': 1, 'jumps': 1, 'over': 1, 'lazy': 1, 'dog': 1}"""


def count_word_frequency(sentence):
    result = {}

    for word in sentence.split():
        result[word] = result.get(word, 0) +1
    return result

print(count_word_frequency("hello world hello"))
print(count_word_frequency("the quick brown fox jumps over the lazy dog"))


"""
Check if Tuple is Palindromic
Design a Python function named is_palindromic_tuple to check if a tuple is palindromic, meaning it reads the same forwards and backwards.

Parameters:
tup (tuple): The input tuple that you need to check for palindromic property.

Returns:
True if the tuple is palindromic, False otherwise.

Example:

Input: (1, 2, 3, 2, 1)
Output: True
Input: ('a', 'b', 'c', 'b', 'a')
Output: True
Input: (1, 2, 3, 4, 5)
Output: False
Input: ('x', 'y', 'z', 'x')
Output: False
Input: ('a',)
Output: True"""

def is_palindromic_tuple(tup):
    i = 0
    j = len(tup)-1
    while i <= j:
        if tup[i] != tup[j]:
            return False
        else:
            i +=1
            j -= 1
    return True

print(is_palindromic_tuple((1, 2, 3, 2, 1)))
print(is_palindromic_tuple(('a', 'b', 'c', 'b', 'a')))
print(is_palindromic_tuple((1, 2, 3, 4, 5)))
print(is_palindromic_tuple(('x', 'y', 'z', 'x')))
print(is_palindromic_tuple(('a',)))


"""
Merge Dictionaries with Overlapping Keys
Design a Python function named merge_dicts_with_overlapping_keys that merges multiple dictionaries into a single dictionary. If a key appears in more than one dictionary, sum up their values.

Parameters:
dicts (list): A list of dictionaries where keys might overlap.

Returns:
A single dictionary where values for overlapping keys are summed.

Example:
Input: [{'a': 1, 'b': 2}, {'b': 3, 'c': 4}, {'c': 5, 'd': 6}]
Output: {'a': 1, 'b': 5, 'c': 9, 'd': 6}
Input: [{'x': 10, 'y': 20}, {'y': 30, 'z': 40}, {'z': 50, 'x': 60}]
Output: {'x': 70, 'y': 50, 'z': 90}
"""

def merge_dicts_with_overlapping_keys(dicts):
    result = {}
    for d in dicts:
        for key, value in d.items():
            result[key] = result.get(key, 0) + value
    return result

print(merge_dicts_with_overlapping_keys([{'a': 1, 'b': 2}, {'b': 3, 'c': 4}, {'c': 5, 'd': 6}]))
print(merge_dicts_with_overlapping_keys([{'x': 10, 'y': 20}, {'y': 30, 'z': 40}, {'z': 50, 'x': 60}]))


"""
Check if a List is a Subset of Another List (Brute Force Approach)
You are given two lists of integers. Write a Python program that checks whether the first list is a subset of the second list using a brute-force approach, without using the in keyword. A list is considered a subset if all elements of the first list are present in the second list.

Parameters:
lst1 (List of integers): The first list, which is being checked as a subset.
lst2 (List of integers): The second list, which is the list to compare against.

Returns:
A boolean value True if lst1 is a subset of lst2, otherwise False.

Example:
Input: lst1 = [1, 2, 3], lst2 = [1, 2, 3, 4, 5]
Output: True
All elements in lst1 are present in lst2.
Input: lst1 = [1, 6], lst2 = [1, 2, 3, 4, 5]
Output: False
The element 6 is not present in lst2.
"""

def is_subset(lst1, lst2):
    for j in lst1:
        if j not in lst2:
            return False

    return True
def counter(arr: list) -> dict:
    result = {}
    for i in arr:
        result[i] = result.get(i, 0) + 1
    return result


def is_subset1(lst1, lst2):
    counter1 = counter(lst1)
    counter2 = counter(lst2)

    for key, value in counter1.items():
        if counter2.get(key,0) < value:
            return False

    return True


print(is_subset1(lst1 = [1, 2, 3], lst2 = [1, 2, 3, 4, 5]))
print(is_subset1(lst1 = [1, 6], lst2 = [1, 2, 3, 4, 5]))