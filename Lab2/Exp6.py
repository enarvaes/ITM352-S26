#Ask the user to enter a temperature in Faherheit
#convert the temperature to Celsius using the formula C = (F - 32) * 5/9
#Name: Ethan Narvaes
#Date: 1/22/2026

fahrenheit_input = input("Enter temperature in Fahrenheit: ")
fahrenheit_value = float(fahrenheit_input)
celsius_value = (fahrenheit_value - 32) * 5 / 9
celsius_value = round(celsius_value, 1)

print(f"You entered {fahrenheit_input} Fahrenheit, which is {celsius_value} Celsius.")