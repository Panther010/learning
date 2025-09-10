"""
Exercise: Python Variables
1. Create a variable called break and assign it a value 5. See what happens and find out the reason behind the behavior that you see.
2. Create two variables. One to store your birth year and another one to store current year. Now calculate your age using these two variables
3. Store your first, middle and last name in three different variables and then print your full name using these variables
4. Answer which of these are invalid variable names: _nation 1record record1 record_one record-one record^one continue
"""

print("Shri Ganesha Namh")

# 1.
# break = 5 ==> invalid syntax

# 2.
birth_year = 1990
current_year = 2025
print(f"My age is {current_year - birth_year}")

# 3.
first_name = "Bakul"
middle_name = ""
last_name = "Seth"
print(f"My name is {first_name} {middle_name} {last_name}")

# 4.
# invalid variable name => 1record, record-one record^one continue

"""
Exercise: Numbers in python
You have a football field that is 92 meter long and 48.8 meter wide. Find out total area using python and print it.
You bought 9 packets of potato chips from a store. Each packet costs 1.49 dollar and you gave shopkeeper 20 dollar. Find out using python, how many dollars is the shopkeeper going to give you back?
You want to replace tiles in your bathroom which is exactly square and 5.5 feet is its length. If tiles cost 500 rs per square feet, how much will be the total cost to replace all tiles. Calculate and print the cost using python (Hint: Use power operator ** to find area of a square)
Print binary representation of number 17
"""

# 1.
length = 92
width = 48.8
print(f"Area of the field is {length * width}")

# 2.
packet_count = 9
packet_cost = 1.49
amount_given = 20
amount_returned = amount_given - (packet_cost * packet_count)
print(f"Shopkeeper going to give me back {amount_returned}")

# 3.
room_length = 5.5
tile_cost = 500
room_area = room_length ** 2
print(f"Total tile cose {room_area * tile_cost}")

# 4.
num = 17
print(f"Binary representation of number {num} is: {format(num, 'b')}")


"""
Exercise: String in Python
Create 3 variables to store street, city and country, now create address variable to store entire address. Use two ways of creating this variable, one using + operator and the other using f-string. Now Print the address in such a way that the street, city and country prints in a separate line
Create a variable to store the string "Earth revolves around the sun"
Print "revolves" using slice operator
Print "sun" using negative index
Create two variables to store how many fruits and vegetables you eat in a day. Now Print "I eat x veggies and y fruits daily" where x and y presents vegetables and fruits that you eat everyday. Use python f string for this.
I have a string variable called s='maine 200 banana khaye'. This of course is a wrong statement, the correct statement is 'maine 10 samosa khaye'. Replace incorrect words in original strong with new ones and print the new string. Also try to do this in one line.
"""

# 1.
street = "Feltham High street"
city = "London"
country = "UK"
address1 = street + "\n" + city + "\n" + country
address2 = f"{street}\n{city}\n{country}"
print(address1, "\n", address2)

# 2.
truth = "Earth revolves around the sun"
print(truth[6:14])
print(truth[-3:])

# 3.
x = 10
y = 15
print(f"I eat {x} veggies and {y} fruits daily")

# 4.
s = 'maine 200 banana khaye'
s = s.replace("banana", "samosa").replace("200", "10")
print(s)