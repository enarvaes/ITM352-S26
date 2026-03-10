# Algorithm for multiplying two numbers by successive addition.

#Changed the function to use a loop to add x to itself y times
def multiply(x, y):
   product = 0
   for products in range(y):
       product += x
  
   return product

#Changed inputs to intergers
first = int(input("Enter the first number: "))
second = int(input("Enter the second number: "))
prod = multiply(first, second)

print(f"The product of {first}, {second} is {prod}")
