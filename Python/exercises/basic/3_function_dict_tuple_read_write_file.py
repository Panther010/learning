"""
Exercise: Functions in python
Write a function called calculate_area that takes base and height as an input and returns and area of a triangle. Equation of an area of a triangle is,
area = (1/2)*base*height
"""
import math

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

"""
Exercise: Python Dict and Tuples
We have following information on countries and their population (population is in crores),

Country	Population
China	143
India	136
USA	32
Pakistan	21
Using above create a dictionary of countries and its population
Write a program that asks user for three type of inputs,
print: if user enter print then it should print all countries with their population in this format,
china==>143
india==>136
usa==>32
pakistan==>21
add: if user input add then it should further ask for a country name to add. If country already exist in our dataset then it should print that it exist and do nothing. If it doesn't then it asks for population and add that new country/population in our dictionary and print it
remove: when user inputs remove it should ask for a country to remove. If country exist in our dictionary then remove it and print new dictionary using format shown above in (a). Else print that country doesn't exist!
query: on this again ask user for which country he or she wants to query. When user inputs that country it will print population of that country.
"""

def population_calculator() -> None:
    country_population = {"China": 143, "India": 136, "USA": 32, "Pakistan": 21}

    first_input = input("Please enter your action : ")

    def print_population() -> None:
        for country, population in country_population.items():
            print(f"{country} ==> {population}")

    def ask_country() -> str:
        return input("Please enter country name : ")

    if first_input == "print":
        print_population()
    elif first_input == "add":
        add_country = ask_country()
        if add_country in country_population:
            print(f"{add_country} already exist")
        else:
            country_population[add_country]=int(input("Please enter country population : "))
            print_population()
    elif first_input == "remove":
        remove_country = ask_country()
        if remove_country in country_population:
            print(f"{country_population.pop(remove_country)} removed from the entry")
            print_population()
        else:
            print(f"country {remove_country} doesn't exist!")
    elif first_input == "query":
        query_country = ask_country()
        if query_country in country_population:
            print(f"Population of {query_country} is {country_population[query_country]}")
        else:
            print(f"country {query_country} doesn't exist!")
    else:
        print("invalid action")
    print("")

# population_calculator()

"""
You are given following list of stocks and their prices in last 3 days,

Stock	Prices
info	[600,630,620]
ril	[1430,1490,1567]
mtl	[234,180,160]
Write a program that asks user for operation. Value of operations could be,
print: When user enters print it should print following,
info ==> [600, 630, 620] ==> avg:  616.67
ril ==> [1430, 1490, 1567] ==> avg:  1495.67
mtl ==> [234, 180, 160] ==> avg:  191.33
add: When user enters 'add', it asks for stock ticker and price. If stock already exist in your list (like info, ril etc) then it will append the price to the list. Otherwise it will create new entry in your dictionary. For example entering 'tata' and 560 will add tata ==> [560] to the dictionary of stocks.
"""

def stock_calculator():
    stock_price = {"info":[600,630,620], "ril": [1430,1490,1567], "mtl": [234,180,160]}
    first_user_in = input("Please give the next operation : ")

    def stock_printer() -> None:
        for stock, price_list in stock_price.items():
            print(f"{stock} ==> {price_list} ==> avg: {sum(price_list)/len(price_list)}")

    if first_user_in == "print":
        stock_printer()
    elif first_user_in == "add":
        stock_ticker = input("Please enter the stock name : ")
        stk_price = int(input("Please enter stock price : "))
        if stock_ticker in stock_price:
            stock_price[stock_ticker].append(stk_price)
        else:
            stock_price[stock_ticker] = [stk_price]

        stock_printer()

# stock_calculator()

"""

Write circle_calc() function that takes radius of a circle as an input from user and then it calculates and returns area, circumference and diameter. You should get these values in your main program by calling circle_calc function and then print them
"""
def circle_calc() -> tuple[float, float, int]:
    radius = int(input("Please enter the radius of circle : "))
    area = math.pi * (radius ** 2)
    circumference = 2 * math.pi * radius
    diameter = 2 * radius

    return area, circumference, diameter

received_data = circle_calc()
print(f"Area of teh circle => {received_data[0]} Circumference of area => {received_data[1]} diameter of area = {received_data[2]}")