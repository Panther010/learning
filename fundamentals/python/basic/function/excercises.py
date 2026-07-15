"""
Celsius to Fahrenheit
Problem Description:

You are given a temperature in Celsius. Your task is to convert it to Fahrenheit and return the result.

Formula:
To convert Celsius to Fahrenheit, use the formula:
F = (9/5 * C) + 32
Where F is the temperature in Fahrenheit and C is the temperature in Celsius.

Input:
A floating-point number C representing the temperature in Celsius.

Output:
A floating-point number representing the temperature in Fahrenheit.

Example:

Input: C = 25
Output: 77.0
Input: C = 0
Output: 32.0
"""


def celsius_to_fahrenheit(c:float) -> float:
    return ((9 / 5) * c) + 32

print(celsius_to_fahrenheit(25))


"""
Area of a Rectangle
Problem Description:

You are given the length and breadth of a rectangle. Your task is to compute and return the area of the rectangle.
Formula:
To calculate the area of a rectangle:
Area=length×breadth

Input:
Two floating-point numbers, length and breadth, representing the dimensions of the rectangle.

Output:
A floating-point number representing the area of the rectangle.

Example:
Input: length = 5, breadth = 3
Output: 15.0
 Input: length = 7.5, breadth = 2.4
Output: 18.0"""

def area_of_rectangle(length: float, breadth: float) -> float:
    return length * breadth

print(area_of_rectangle(5, 3))

"""
Distance covered by a Vehicle
Problem Description:
You are given the speed of a vehicle and the time it has traveled. Your task is to compute and return the distance traveled by the vehicle.

Formula:
To calculate the distance traveled by a vehicle:
Distance=Speed×Time

Input:
Two floating-point numbers, speed and time, representing the speed of the vehicle and the time it has been traveling.

Output:
A floating-point number representing the distance traveled.

Example:
Input: speed = 60, time = 2
Output: 120.0
 
Input: speed = 50.5, time = 1.5
Output: 75.75
"""
def calculate_distance(speed: float, time: float) -> float:
    return speed * time * 1.0

print(calculate_distance(60, 3))


"""
Number of Rounds of Lift
Problem Description:

You are given n, the total number of people, and capacity, the maximum number of people the lift can carry at a time. All people want to go from the ground floor to the top floor. Your task is to calculate the number of rounds the lift has to make to transport all the people to the top floor.

Input:
Two integers, n and capacity, where n is the total number of people, and capacity is the maximum number of people the lift can carry in one round.

Output:
An integer representing the number of rounds the lift needs to cover to transport all people to the top floor.

Example:

Input: n = 10, capacity = 3
Output: 4
 
Input: n = 7, capacity = 4
Output: 2


"""
def calculate_lift_rounds(n, capacity):
    return (n + capacity - 1) // capacity

"""
Line Equation
Problem Description:

You are given the slope m and the y-intercept b of a line, along with a value x. Your task is to calculate and return the value of y using the equation of a line in slope-intercept form:
y=mx+b

Input:
Three floating-point numbers: slope, intercept, and x.

Output:
A floating-point number representing the value of yyy corresponding to the given xxx.

Example:

Input: slope = 2, intercept = 3, x = 4
Output: 11.0
Input: slope = 1.5, intercept = -2, x = 2
Output: 1.0
"""
def calculate_y(slope, intercept, x):
    return slope * x + intercept