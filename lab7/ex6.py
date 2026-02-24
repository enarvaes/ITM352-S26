#data = ("hello", 10, "goodbye", "3", "goodnight", 5, 6.7, True)
#user_input = input("Enter something to add to the tuple: ")
#data.append(user_input)
#print(data)


data = ("hello", 10, "goodbye", "3", "goodnight", 5, 6.7, True)
new_val = input("Enter a value to append: ")
data = data + (new_val,)
print("Updated tuple (Concatenation):", data)
