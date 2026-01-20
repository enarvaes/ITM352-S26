def add(x, y):
    """Add two numbers."""
    return x + y


def subtract(x, y):
    """Subtract two numbers."""
    return x - y


def multiply(x, y):
    """Multiply two numbers."""
    return x * y


def divide(x, y):
    """Divide two numbers."""
    if y == 0:
        return "Error: Division by zero"
    return x / y


operations = {
    '1': (add, '+'),
    '2': (subtract, '-'),
    '3': (multiply, '*'),
    '4': (divide, '/')
}


def main():
    """Main function to run the calculator."""
    print("Simple Calculator")
    print("-" * 30)
    print("Select operation:")
    for key in operations:
        op_name = ['Add', 'Subtract', 'Multiply', 'Divide'][int(key) - 1]
        print(f"{key}. {op_name}")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter choice (1/2/3/4/5): ")
        
        if choice == '5':
            print("Thank you for using the calculator!")
            break
        
        if choice in operations:
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                
                func, symbol = operations[choice]
                result = func(num1, num2)
                print(f"{num1} {symbol} {num2} = {result}")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
