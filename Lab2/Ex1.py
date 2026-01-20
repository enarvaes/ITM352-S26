#Ask the user for a number between 1 and 100. Square the number and print the number and its square
#Name: Ethan Narvaes
#Date 1/20/2026

usersnum = int(input("Enter a number 1 - 100: "))
if usersnum < 100 or usersnum > 1:
    #print(usersnum, "squared =", usersnum **2)
    print(f"{usersnum} squared = {usersnum **2}")

else:
    print("Number not in range.")