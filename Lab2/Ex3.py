#Ask the user to eneter a floating point number, square the number
#Print out the original number and its square result
#Name: Ethan Narvaes
#Date: 1/22/2026

input_value = input("Enter a floating point number: ")
float_value = float(input_value)
squared_value = float_value ** 2

#Round the number to 2 decimal places
squared_value = round(squared_value, 2)

print(f"{input_value} squared = {squared_value}")