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
