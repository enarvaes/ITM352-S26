# Calculating a shopping cart

#Made sure the total price when adding to a previous value rather 
#than resetting it to the current price
prices = [5.95, 3.00, 12.50]
total_price = 0
tax_rate = 1.08    # 8% tax 
for price in prices:
    total_price += price * tax_rate


#Fixed Formatting for the when printing out price (2 decimols)
print(f"Total price (with tax): ${total_price:.2f}")