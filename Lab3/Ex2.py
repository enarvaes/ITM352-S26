#Create a function called midpoint

def midpoint(num1, num2):
    """Calculate the midpoint between two numbers."""
    return (num1 + num2) / 2

number1 = float(input("Enter the first number: "))
number2 = float(input("Enter the second number: ")) 
results = midpoint(number1, number2)
print(f"The midpoint between {number1} and {number2} is {results}.")