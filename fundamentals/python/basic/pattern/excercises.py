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



"""
Problem Description:
You are given an integer n. Your task is to return a right-angled triangle pattern of '*' where each side has n characters, represented as a list of strings. The triangle has '*' characters, starting with 1 star in the first row, 2 stars in the second row, and so on until the last row has n stars.

Input Parameters:
n (int): The height and base of the right-angled triangle.

Output:
A list of strings where each string is a row of '*' characters that increases in length from 1 to n.

Example:
Input: 3
Output: ['*', '**', '***']
 
Input: 5
Output: ['*', '**', '***', '****', '*****']
"""
def generate_triangle(n: int):
    return ["*" * (i + 1) for i in range(n)]

print(generate_triangle(3))
print(generate_triangle(5))


"""
Problem Description:
You are given an integer n. Your task is to return an inverted right-angled triangle pattern of '*' where each side has n characters, represented as a list of strings. The first row should have n stars, the second row n-1 stars, and so on, until the last row has 1 star.

Input Parameters:
n (int): The height and base of the inverted right-angled triangle.

Output:
A list of strings where each string is a row of '*' characters that decreases in length from n to 1.

Example:

Input: 3
Output: ['***', '**', '*']
 Input: 5
Output: ['*****', '****', '***', '**', '*']
"""
def generate_inverted_triangle(n):
    return ["*" * i for i in range(n, 0, -1)]

print(generate_inverted_triangle(3))
print(generate_inverted_triangle(5))


"""
Problem Description:
You are given an integer n. Your task is to return a pyramid pattern of '*' where each side has n rows, represented as a list of strings. The pyramid is centered, with 1 star in the first row, 3 stars in the second row, and so on, increasing by 2 stars per row until the base row has 2n - 1 stars.

Input:
A single integer n, where 1 <= n <= 100.

Output:
A list of strings where each string contains stars ('*') centered, forming a pyramid shape. Each row has an increasing number of stars, with appropriate spaces for centering.

Example:

Input: 3
Output: ['  *  ', ' *** ', '*****']
 
Input: 5
Output: ['    *    ', '   ***   ', '  *****  ', ' ******* ', '*********']
"""
def generate_pyramid(n):
    result = []
    for i in range(n):
        spaces = " " *  (n - i - 1)
        stars = "*" * (2 * i + 1)
        result.append(spaces + stars + spaces)

    return result
print(generate_pyramid(3))
print(generate_pyramid(4))
print(generate_pyramid(5))



"""
Problem Description
You are given an integer n. Your task is to return an inverted pyramid pattern of '*', where each side has n rows, represented as a list of strings. The first row has 2n - 1 stars, the second row has 2n - 3 stars, and so on, until the last row has 1 star, with each row centered using spaces.

Input Parameters:
n (int): The number of rows in the inverted pyramid.

Output:
A list of strings where each string represents a row of the inverted pyramid.

Example:
Input: 3
Output: ['*****', ' *** ', '  *  ']
Input: 5
Output: ['*********', ' ******* ', '  *****  ', '   ***   ', '    *    ']

"""
def generate_inverted_pyramid(n:int):
    result = []
    for i in range(n):
        spaces = " " *  (i)
        stars = "*" * (2 * n - 1 - (2*i))
        result.append(spaces + stars + spaces)

    return result

print(generate_inverted_pyramid(3))
print(generate_inverted_pyramid(5))


"""
Problem Description:
You are given an integer n. Your task is to return a right-angled triangle pattern where each row contains repeated digits. The first row contains the number 1 repeated once, the second row contains the number 2 repeated twice, and so on until the nth row contains the number n repeated n times.

Input:
A single integer n, where 1 <= n <= 100.

Output:
A list of strings where each string represents a row in the triangle. The ith row contains the digit i repeated i times.

Example:

Input: 5
Output: ['1', '22', '333', '4444', '55555']
 
Input: 3
Output: ['1', '22', '333']

"""

def generate_number_triangle(n):
    result = []
    for i in range(n):
        result.append(str(i+1) * (i+1))

    return result

print(generate_number_triangle(5))


"""
Problem Description:
You are given an integer n. Your task is to return the first n rows of Floyd’s Triangle, represented as a list of strings. Floyd's Triangle is a triangular array of natural numbers where the first row contains 1, the second row contains 2 and 3, the third row contains 4, 5, and 6, and so on.

Input:
A single integer n, where 1 <= n <= 100.

Output:
A list of strings where each string represents a row in Floyd's Triangle.

Example:
Input: 5
Output: ['1', '2 3', '4 5 6', '7 8 9 10', '11 12 13 14 15']
Input: 3
Output: ['1', '2 3', '4 5 6']
"""

def generate_floyds_triangle(n):
    result = []
    current_num = 1
    row = ""
    for i in range(n):
        for j in range(i+1):
            row = row + str(current_num) + " "
            current_num += 1
        result.append(row)
        row = ""
    return result
print(generate_floyds_triangle(3))
print(generate_floyds_triangle(5))