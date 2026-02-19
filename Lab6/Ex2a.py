my_list = ["apple", 42, 3.14, True, "banana", 7]

if len(my_list) < 5:
    print("Fewer than 5 elements")
elif 5 <= len(my_list) <= 10:
    print("Between 5 and 10 elements (inclusive)")
else:
    print("More than 10 elements")