"""
Problem Description:
You are given a string s. Your task is to return the reversed version of the string.

Input:
A single string s, where the length of s is between 1 and 1000.

Output:
A single string that is the reverse of the input string.

Example:
Input: "hello"
Output: "olleh"
Input: "Python"
Output: "nohtyP"
"""

def reverse_string(s: str) -> str :
    result = ""
    for char in s:
        result = char+result

    return result

print(reverse_string("hello"))
print(reverse_string("Python"))


"""
Problem Description:
You are given a string s. Your task is to count the number of vowels (both uppercase and lowercase) in the string and return the total count.

Input:
A single string s, where the length of s is between 1 and 1000.

Output:
An integer representing the total count of vowels in the input string.

Example:
Input: "Hello, World!"
Output: 3
Input: "Python Programming"
Output: 4
"""
def count_vowels(s: str) -> int:
    count = 0
    vowels = "aeiou"

    for char in s:
        if char.lower() in vowels:
            count+= 1
    return count
print(count_vowels("Hello, World!"))
print(count_vowels("Python Programming"))

"""
Problem Description:
You are given a string s. Your task is to check if the string is a palindrome. A string is considered a palindrome if it reads the same forward and backward, ignoring spaces, punctuation, and case.

Input:
A single string s, where the length of s is between 1 and 1000.

Output:
A boolean value: True if the string is a palindrome, and False otherwise.

Example:
Input: "A man a plan a canal Panama"
Output: True
Input: "Hello, World!"
Output: False
"""
def is_palindrome(s: str) -> bool:
    s = s.replace(" ", "").lower()
    i = 0
    length = len(s)-1
    while i <= length:
        if s[i] != s[length]:
            return False
        i+=1
        length-=1
    return True

print(is_palindrome("Hello, World!"))
print(is_palindrome("A man a plan a canal Panama"))


"""
Problem Description:
You are given a string s. Your task is to count the number of words in the string and return the total count. A word is defined as a sequence of characters separated by spaces.

Input:
A single string s, where the length of s is between 1 and 1000.

Output:
An integer representing the total count of words in the input string.

Example:
Input: "Hello, World!"
Output: 2
Input: "Python programming is fun."
Output: 4
"""
def count_words(s: str) -> int:
    count = 0

    return len(s.split())

"""
Problem Description:
You are given a string s. Your task is to remove duplicate characters from the string while preserving the order of the first occurrences and return the modified string.

Input:
A single string s, where the length of s is between 1 and 1000.

Output:
A string that contains only the first occurrence of each character from the input string.

Example:
Input: "programming"
Output: "progamin"
Input: "Hello, World!"
Output: "Helo, Wrd!"
"""
def remove_duplicates(s: str) -> str:
    result = []
    seen = set()

    for char in s:
        if char not in seen:
            result.append(char)
            seen.add(char)
    return "".join(result)

print(remove_duplicates("programming"))
print(remove_duplicates("Hello, World!"))


"""
Problem Description:
You are given a string s. Your task is to count the number of consonants in the string and return the total count. A consonant is any alphabetic character that is not a vowel (a, e, i, o, u).

Input:
A single string s, where the length of s is between 1 and 1000.

Output:
An integer representing the total count of consonants in the input string.

Example:
Input: "Hello, World!"
Output: 7
Input: "Python Programming"
Output: 13
"""

def count_consonants(s):
    vowels = {"a", "e", "i", "o", "u"}
    return sum(1 for c in s.lower() if c not in vowels and c.isalpha())

print(count_consonants("Hello, World!"))
print(count_consonants("Python Programming"))


"""Problem Description:
You are given two strings s and t. Your task is to determine if string t is an anagram of string s. An anagram is a word or phrase formed by rearranging the characters of a different word or phrase, using all the original characters exactly once.

Input:
Two strings s and t where both lengths are between 1 and 1000.

Output:
Return True if t is an anagram of s, and False otherwise.

Example:
Input: s = "anagram", t = "nagaram"
Output: True
Input: s = "rat", t = "car"
Output: False
"""
def is_anagram(s: str, t:str) -> bool:
    s = s.replace(" ", "").lower()
    t = t.replace(" ", "").lower()

    if len(s) != len(t):
        return False

    counter = {}
    for i in s:
        counter[i] = counter.get(i, 0) + 1

    for j in t:
        if j not in counter or counter[j] == 0:
            return False
        counter[j] -= 1

    return True

print(is_anagram(s="anagram", t="nagaram"))
print(is_anagram(s="rat", t="car"))


"""
Problem Description:
You are given two strings s and t. Your task is to determine if string t is a subsequence of string s. A subsequence of a string is a new string that is formed from the original string by deleting some (or no) characters without changing the order of the remaining characters.

Input:
Two strings s and t where the length of s is between 1 and 1000, and the length of t is between 1 and 1000.

Output:
Return True if t is a subsequence of s, and False otherwise.

Example:
Input: s = "abcde", t = "ace"
Output: True
Input: s = "abcde", t = "aec"
Output: False
"""

def is_subsequence(s, t):
    if not t:
        return True

    s_pointer = t_pointer = 0

    while s_pointer < len(s) and t_pointer < len(t):
        if s[s_pointer] == t[t_pointer]:
            t_pointer += 1

        s_pointer += 1

    return t_pointer == len(t)

print(is_subsequence(s = "abcde", t = "ace"))
print(is_subsequence(s = "abcde", t = "aec"))


"""
Problem Description:
You are given two strings, s and t. Your task is to determine if the string t is a substring of the string s. A substring is a contiguous sequence of characters within a string. Do not use any built-in functions for string operations and do not use recursion.

Input:
Two strings s and t, where 1 <= len(s), len(t) <= 1000.

Output:
A boolean value (True or False) indicating whether t is a substring of s.


Example:
Input: s = "hello world", t = "world"
Output: True
Input: s = "hello world", t = "worlds"
Output: False
"""
def is_substring(s, t):
    s_length, t_length = len(s), len(t)

    for i in range(s_length - t_length + 1):
        if s[i: i+t_length] == t:
            return True
    return False

print(is_substring(s = "hello world", t = "world"))
print(is_substring(s = "hello world", t = "worlds"))


"""
Problem Description:
You are given a string s. Your task is to find the length of the longest word in the string. A word is defined as a sequence of characters separated by spaces. Do not use any built-in functions for string manipulation.

Input:
A string s, where the length of s is between 1 and 1000 characters.

Output:
An integer representing the length of the longest word in the string.

Example:
Input: s = "The quick brown fox jumps over the lazy dog"
Output: 5
Input: s = "Hello World"
Output: 5
"""

def longest_word_length(s):
    result = 0
    word_length = 0
    for char in s:
        if char == " ":
            result = max(result, word_length)
            word_length = 0
        else:
            word_length += 1

    return max(result, word_length)

def longest_word_length1(s):
    result = 0
    for word in s.split():
        result = max(result, len(word))

    return result

print(longest_word_length(s = "The quick brown fox jumps over the lazy dog"))
print(longest_word_length(s = "Hello World"))