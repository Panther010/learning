"""
Problem Description:
You are given an integer n. Your task is to calculate and return the sum of the first n even natural numbers. The even natural numbers are: 2, 4, 6, 8, ...

Input:
A single integer n where 1 <= n <= 10^4.

Output:
Return the sum of the first n even natural numbers.

Example:
Input: n = 3
Output: 12  # (2 + 4 + 6)
 Input: n = 5
Output: 30  # (2 + 4 + 6 + 8 + 10)
"""
import math


def sum_of_even_numbers(n):
    if n ==0:
        return 0
    result = 0
    for i in range(n):
        result += ((i+1)*2)
    return result

print(sum_of_even_numbers(3))
print(sum_of_even_numbers(5))


"""
Problem Description:
You are given an integer n. Your task is to check whether the number is even or not. Return True if the number is even, and False otherwise.

Input:
A single integer n where -10^9 <= n <= 10^9.

Output:
Return True if n is an even number, otherwise return False.

Example:
Input: n = 4
Output: True
Input: n = 7
Output: False
"""
def is_even(n):
    return n % 2 == 0

print(is_even(4))
print(is_even(7))


"""
Problem Description:
You are given an integer n. Your task is to check whether the number is prime or not. A prime number is a number greater than 1 that has no divisors other than 1 and itself. Return True if the number is prime, and False otherwise.

Input:
A single integer n where 1 <= n <= 10^6.

Output:
Return True if n is a prime number, otherwise return False.

Example:
Input: n = 5
Output: True
 Input: n = 4
Output: False"""
def is_prime(n):
    if n<=2:
        return False
    if n==2 or n==3:
        return True
    if n%2==0:
        return False
    if n%3==0:
        return False

    max_divisor = int(math.sqrt(n))
    for d in range(3, max_divisor+1, 2):
        if n%d==0:
            return False

    return True

print(is_prime(11))  # Returns: True
print(is_prime(4))   # Returns: False
print(is_prime(1))   # Returns: False


"""
Problem Description:
You are given a positive integer num. Your task is to check whether num is a perfect square or not. A perfect square is an integer that is the square of an integer (e.g., 1, 4, 9, 16, ...). Return True if num is a perfect square, and False otherwise.

Input:
A single positive integer num where 1 <= num <= 10^9.

Output:
Return True if num is a perfect square, otherwise return False.

Example:
Input: num = 16
Output: True
 Input: num = 14
Output: False"""
def is_perfect_square(num):
    return int(math.sqrt(num)) == math.sqrt(num)

print(is_perfect_square(16))
print(is_perfect_square(14))