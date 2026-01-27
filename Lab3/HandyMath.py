#Handy library of math functions
#Name: Ethan Narvaes
#Date: 1/27/2026

def midpoint(num1, num2):
    """Calculate the midpoint between two numbers."""
    return (num1 + num2) / 2

number1 = float(input("Enter the first number: "))
number2 = float(input("Enter the second number: ")) 
results = midpoint(number1, number2)
print(f"The midpoint between {number1} and {number2} is {results}.")

def sqrt(number):
    """Calculate the square root of a number."""
    if number < 0:
        return None
    return number ** 0.5

number_a = float(input("Enter a number a postive number to find the square root: "))
results = sqrt(number_a)
if results is None:
    print("Error: Cannot compute the square root of a negative number.")
else:
    print(f"The square root of {number_a} is {results}.")

def exponent(base, exp, percision):
    """Calculate the exponent of a base raised to exp."""
    result = base ** exp
    rounded_result = round(result, percision)
    return rounded_result