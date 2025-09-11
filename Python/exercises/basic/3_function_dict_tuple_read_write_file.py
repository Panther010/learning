"""
Exercise: Functions in python
Write a function called calculate_area that takes base and height as an input and returns and area of a triangle. Equation of an area of a triangle is,
area = (1/2)*base*height
"""
"""
Modify above function to take third parameter shape type. It can be either "triangle" or "rectangle". Based on shape type it will calculate area. Equation of rectangle's area is,
rectangle area=length*width
If no shape is supplied then it should take triangle as a default shape
"""
"""
Write a function called print_pattern that takes integer number as an argument and prints following pattern if input number is 3,
*
**
***
if input is 4 then it should print
"""
"""
*
**
***
****
Basically number of lines it prints is equal to that number. (Hint: you need to use two for loops)
"""

def area_calculator(base, height, shape ='triangle') -> float:
    area = 0
    if shape == 'rectangle':
        area = base * height
    elif shape == 'triangle':
        area = .5 * base * height
    else:
        print(f"Error: Input shape is unknown")
    return area

print(area_calculator(5, 15, 'rectangle'))
print(area_calculator(5, 15, 'triangle'))
print(area_calculator(5, 15, ))
print(area_calculator(5, 15, 'jksdhbv'))

def pattern_printer(lines: int) -> None:
    for i in range(lines):
        print('*' * (i+1))

def pattern_printer2(lines: int) -> None:
    for i in range(1, lines+1):
        for j in range(i):
            print('*', end='')

        print('')

pattern_printer2(5)