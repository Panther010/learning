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


"""
Problem Description:
You are given an integer n. Your task is to return its binary representation as a string. Do not use any built-in functions for conversion.

Input:
A single integer n, where -10^9 <= n <= 10^9.

Output:
A string representing the binary representation of n.


Example:
Input: n = 5
Output: "101"
Input: n = -5
Output: "-101"
"""
def int_to_binary(n):
    result = ""
    if n ==0:
        return "0"
    is_negative = n < 0
    n = abs(n)

    while n>0:
        result+=str(n%2)
        n=n//2
    return f"-{result}" if is_negative else result


print(int_to_binary(7))
print(int_to_binary(5))
print(int_to_binary(-5))


"""
Problem Description:
You are given a string binary_str representing a binary number. Your task is to convert this binary string to its corresponding decimal integer. Do not use any built-in functions for conversion.

Input:
A string binary_str, consisting of characters '0' and '1', where the length of the string is between 1 and 30 (inclusive).

Output:
An integer representing the decimal value of the binary string

Example:

Input: binary_str = "101"
Output: 5
 Input: binary_str = "1101"
Output: 13
"""
def binary_to_decimal(binary_str):
    result = counter = 0
    bin_num = int(binary_str)

    if bin_num < 2:
        return bin_num

    while bin_num>0:
        n = bin_num%10
        bin_num = bin_num//10
        result = 2**counter * n +result
        print(n, bin_num, result, counter)
        counter += 1

    return result


def binary_to_decimal1(binary_str):
    result = 0
    for n in binary_str:
        result = 2*result+int(n)

    return result

print(binary_to_decimal1("1111"))
print(binary_to_decimal1("1110"))


"""
Problem Description:
You are given two integers n and m. Your task is to find the GCD of these two numbers. The GCD is the largest positive integer that divides both numbers without leaving a remainder. Do not use any built-in functions and do not use recursion.

Input:
Two integers n and m, where 1 <= n, m <= 10^9.

Output:
An integer representing the GCD of n and m.

Example:
Input: n = 48, m = 18
Output: 6
Input: n = 56, m = 98
Output: 14
"""
def gcd(n, m):
    print(n, m)

    while m > 0:
        n, m = m , n % m
        print(n, m)
    return n

print(gcd(48, 18))
print(gcd(56, 98))

def lcm(n, m):
    if  n == 0 or m == 0:
        return 0
    return (n//gcd(n,m)) * m

print(lcm(48, 18))
print(lcm(56, 98))
