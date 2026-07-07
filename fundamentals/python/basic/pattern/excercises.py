"""
Problem Description: You are given an integer n. Your task is to return a square pattern of size n x n made up of the character '*', represented as a list of strings.

Input Parameters:
n (int): The size of the square (number of rows and columns).

Output:
A list of strings where each string is a row of n characters.

Example:
Input: 3
Output: ['***', '***', '***']

Input: 5
Output: ['*****', '*****', '*****', '*****', '*****']

"""
def square_of_n_side(n: int) -> list[str]:
    return ["*" * n for _ in range(n)]

print(square_of_n_side(5))



"""
Problem Description:
You are given an integer n. Your task is to return a hollow square pattern of size n x n made up of the character '*', represented as a list of strings. The hollow square has '*' on the border, and spaces ' ' in the middle (except for side lengths of 1 and 2).

Input Parameters:
n (int): The size of the square (number of rows and columns).

Output:
A list of strings where each string is a row of n characters, representing a hollow square.

Example:
Input: 3
Output: ['***', '* *', '***']
 
Input: 5
Output: ['*****', '*   *', '*   *', '*   *', '*****']
"""
def hollow_square_of_n_side(n: int) -> list[str]:
    if n == 0:
        return []
    if n == 1:
        return ["*"]

    result = []
    start_and_end = "*" * n
    middle = "*" + " " * (n-2) + "*"
    result.append(start_and_end)
    for _ in range(n-2):
        result.append(middle)

    result.append(start_and_end)
    return result

print(hollow_square_of_n_side(2))




"""
Problem Description:
You are given two integers, n and m. Your task is to return a rectangle pattern of '*', where n represents the number of rows (length) and m represents the number of columns (breadth).

Input:
Two integers n and m, where 1 <= n, m <= 100.

Output:
A list of strings where each string represents a row of the rectangle pattern.

Example:
Input: n = 4, m = 5
Output: ['*****', '*****', '*****', '*****']
 
Input: n = 3, m = 2
Output: ['**', '**', '**']
"""
def generate_rectangle(n: int, m: int) -> list[str]:
    return ["*" * m for _ in range(n)]

print(generate_rectangle(4, 5))