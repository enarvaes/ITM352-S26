#Handy library of math functions
#Name: Ethan Narvaes
#Date: 1/27/2026

def midpoint(num1, num2):
    """Calculate the midpoint between two numbers."""
    return (num1 + num2) / 2

def sqrt(number):
    """Calculate the square root of a number."""
    if number < 0:
        return None
    return number ** 0.5

def exponent(base, exp, percision=2):
    """Calculate the exponent of a base raised to exp."""
    result = base ** exp
    rounded_result = round(result, percision)
    return rounded_result

def max(num1, num2):
    """Return the maximum of two numbers."""
    return num1 if num1 > num2 else num2

def min(num1, num2):
    """Return the minimum of two numbers."""
    return num1 if num1 < num2 else num2