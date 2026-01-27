#This program demonstrates variable scope in Python.
#Name: Ethan Narvaes
#Date: 1/27/2026

def calculate_discounted_price(price, discount):
    price = price * discount
    print(f"Inside the function, discount price: {price:.2f}")
    return price

discount = 0.6
price = 100.0
print(f"Original price before function call: {price:.2f}")
discounted__price = calculate_discounted_price(price, discount)

print(f"Original price after function call: {price:.2f}")
print (f"Discount={discount}")