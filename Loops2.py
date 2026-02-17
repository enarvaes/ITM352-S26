prices = [100, 50, 20, 356]

total = 0

itemcount = 0

for price in prices:
    itemcount += 1
    if itemcount > 2:
        discounted_price = price * 0.9  # Apply a 10% discount
    else:
        discounted_price = price
    total += discounted_price

rounded_total = round(total, 2)  # Round the total to 2 decimal places
print(f"Total price: ${rounded_total:,.2f}")