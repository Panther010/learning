"""
Exercise: Python Lists
Let us say your expense for every month are listed below,
January - 2200
February - 2350
March - 2600
April - 2130
May - 2190
Create a list to store these monthly expenses and using that find out,

1. In Feb, how many dollars you spent extra compare to January?
2. Find out your total expense in first quarter (first three months) of the year.
3. Find out if you spent exactly 2000 dollars in any month
4. June month just finished and your expense is 1980 dollar. Add this item to our monthly expense list
5. You returned an item that you bought in a month of April and got a refund of 200$. Make a correction to your monthly expense list based on this
"""
from operator import index

"""
You have a list of your favourite marvel super heros.
heros=['spider man','thor','hulk','iron man','captain america']
Using this find out,
1. Length of the list
2. Add 'black panther' at the end of this list
3. You realize that you need to add 'black panther' after 'hulk', so remove it from the list first and then add it after 'hulk'
4. Now you don't like thor and hulk because they get angry easily :) So you want to remove thor and hulk from list and replace them with doctor strange (because he is cool). Do that with one line of code.
5. Sort the heros list in alphabetical order (Hint. Use dir() functions to list down all functions available in list)
"""
# 1.
def list1() -> None :
    expense = [2200, 2350, 2600, 2130, 2190]

    # 1. In Feb, how many dollars you spent extra compare to January?
    print(f"In Feb, I spent {expense[1] - expense[0]} dollar extra compare to January")

    # 2. Find out your total expense in first quarter (first three months) of the year.
    print(f"Total expense in first quarter is {sum(expense[:3])}")

    # 3. Find out if you spent exactly 2000 dollars in any month
    print(f"If I have spent exactly 2000 dollars in any month {2000 in expense}")

    # 4. June month just finished and your expense is 1980 dollar. Add this item to our monthly expense list
    expense.append(1980)
    print(f"new expense detail {expense}")

    # 5. You returned an item that you bought in a month of April and got a refund of 200$. Make a correction to your monthly expense list based on this
    expense[3] = expense[3] - 200
    print(f"Updated expense after refund is {expense}")

def list2() -> None :
    heros: list[str] = ['spider man','thor','hulk','iron man','captain america']

    # 1. Length of the list
    print(f"Length of the list is {len(heros)}")

    # 2. Add 'black panther' at the end of this list
    heros.append("black panther")
    print(f"Updated list of heros is {heros}")

    # 3. You realize that you need to add 'black panther' after 'hulk', so remove it from the list first and then add it after 'hulk'
    print(f"removing {heros.pop()} from the list. Now list is {heros}")
    heros.insert(3, "black panther")
    print(f"Updated list after adding panther after hulk {heros}")

    # 4. Now you don't like thor and hulk because they get angry easily :) So you want to remove thor and hulk from list and replace them with doctor strange (because he is cool). Do that with one line of code.
    heros[1:3] = ["doctor strange"]
    print(f"Updated lsi after adding Dr strange {heros}")

    # 5. Sort the heros list in alphabetical order (Hint. Use dir() functions to list down all functions available in list)
    heros.sort()
    print(heros)

# list1()
# list2()

"""
1. Using following list of cities per country,
india = ["mumbai", "banglore", "chennai", "delhi"]
pakistan = ["lahore","karachi","islamabad"]
bangladesh = ["dhaka", "khulna", "rangpur"]
Write a program that asks user to enter a city name and it should tell which country the city belongs to
Write a program that asks user to enter two cities and it tells you if they both are in same country or not. For example if I enter mumbai and chennai, it will print "Both cities are in India" but if I enter mumbai and dhaka it should print "They don't belong to same country"
"""
"""2. Write a python program that can tell you if your sugar is normal or not. Normal fasting level sugar range is 80 to 100.
Ask user to enter his fasting sugar level
If it is below 80 to 100 range then print that sugar is low
If it is above 100 then print that it is high otherwise print that it is normal
"""

def city_if() -> None :
    # Write a program that asks user to enter a city name and it should tell which country the city belongs to
    india = ["mumbai", "banglore", "chennai", "delhi"]
    pakistan = ["lahore","karachi","islamabad"]
    bangladesh = ["dhaka", "khulna", "rangpur"]

    user_input = input("Please enter city name : ")
    if user_input in india:
        print(f"City {user_input} is present in India.")
    elif user_input in pakistan:
        print(f"City {user_input} is in pakistan")
    elif user_input in bangladesh:
        print(f"City {user_input} is in Bangladesh")
    else:
        print("Unknown city")

    # Write a program that asks user to enter two cities and it tells you if they both are in same country or not. For example if I enter mumbai and chennai, it will print "Both cities are in India" but if I enter mumbai and dhaka it should print "They don't belong to same country"
    city1 = input("Please enter city 1 : ")
    city2 = input("Please enter city 2 : ")

    if city1 in india and city2 in india:
        print(f"{city1} and {city2} are present in India.")
    elif city1 in pakistan and city2 in pakistan:
        print(f"{city1} and {city2} are in pakistan")
    elif city1 in bangladesh and city2 in bangladesh:
        print(f"{city1} and {city2} are in Bangladesh")
    else:
        print(f"{city1} and {city2} are not in same country")

def sugar_check() -> None:
    sugar_level = int(input("Please enter fasting sugar level : "))
    if sugar_level < 80:
        print("Sugar is low")
    elif sugar_level > 100:
        print("Sugar is high")
    else:
        print("Sugar is normal")
# city_if()
# sugar_check()

"""
Exercise: Python for loop
After flipping a coin 10 times you got this result,
result = ["heads","tails","tails","heads","tails","heads","heads","tails","tails","tails"]
Using for loop figure out how many times you got heads
"""
"""
Print square of all numbers between 1 to 10 except even numbers
Your monthly expense list (from Jan to May) looks like this,
expense_list = [2340, 2500, 2100, 3100, 2980]
Write a program that asks you to enter an expense amount and program should tell you in which month that expense occurred. If expense is not found then it should print that as well.
"""
"""
Lets say you are running a 5 km race. Write a program that,
"""
"""
Upon completing each 1 km asks you "are you tired?"
If you reply "yes" then it should break and print "you didn't finish the race"
If you reply "no" then it should continue and ask "are you tired" on every km
If you finish all 5 km then it should print congratulations message
Write a program that prints following shape

*
**
***
****
*****

"""

# 1.
def for1() -> None:
    result = ["heads","tails","tails","heads","tails","heads","heads","tails","tails","tails"]
    counter = 0
    for i in result:
        if i == 'heads':
            counter += 1

    print(f"{counter} times we got heads")

    for n in range(1, 11):
        print(n**2)

def for2() -> None:
    expense_list = [2340, 2500, 2100, 3100, 2980]
    user_expense = int(input("Please enter expense: "))
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    if user_expense in expense_list:
        print(f"you spent {user_expense} in {months[expense_list.index(user_expense)]} month")
    else:
        print(f"You have not spent {user_expense} in any month")

def for3() -> None:

    for i in range(1,6):
        if i == 5:
            print(f"Congratulations you have completed the race")
        else:
            tired = input(f"Are you tired after {i} KMs: ")
            if tired == 'yes':
                print(f"You didn't finish 5 km race but hey congrats anyways! you completed {i} kms")
                break


def for4() -> None:
    for i in range(1,6):
        print('*' * i)

for4()