# String manipulation examples
# Name: Ethan Narvaes
# Date: Jan 29, 2026

# 1. Input Section
first = input("Enter your first name: ")
middleIn = input("Enter your middle initial: ")
last = input("Enter your last name: ")

# 2. Concatenation using "+"
# Note: Python knows this is string concatenation because the variables are 'str' types.
# If they were integers, it would perform mathematical addition.
full_name_plus = first + " " + middleIn + " " + last
print("1. Plus Operator:  ", full_name_plus)

# 3. Concatenation using f-string
full_name_f = f"{first} {middleIn} {last}"
print("2. f-string:       ", full_name_f)

# 4. Concatenation using % Operator
percent_name = "%s %s %s" % (first, middleIn, last)
print("3. % Operator:     ", percent_name)

# 5. Concatenation using .format() method
format_name = "{} {} {}".format(first, middleIn, last)
print("4. .format() method:", format_name)

# 6. Concatenation using .join() method of a list
# Your image had a small syntax error here; ensure the list is inside the parentheses.
join_name = " ".join([first, middleIn, last])
print("5. .join() method:  ", join_name)

# 7. Concatenation using .format() with unpacking (*)
format_unpacking_list = [first, middleIn, last]
full_name_unpack = "{} {} {}".format(*format_unpacking_list)
print("6. List Unpacking: ", full_name_unpack)