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
    