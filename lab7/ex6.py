#data = ("hello", 10, "goodbye", "3", "goodnight", 5, 6.7, True)
#user_input = input("Enter something to add to the tuple: ")
#data.append(user_input)
#print(data)

data = ("hello", 10, "goodbye", 3, "welcome", 5, 6, 7, True)
user_input = input("Enter something to add: ")
temp_list = list(data)

temp_list.append(user_input)

data = tuple(temp_list)
