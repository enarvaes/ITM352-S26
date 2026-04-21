# Calculating an extended price for a product (with tax)

#Had to turn price into a number rather than a string
product = {
    "name": 'small gumball', 
    "price": 0.34
}

tax_rate = 0.045

total = product["price"] + product["price"] * tax_rate

# Fixed format of pullling information from the product 
# dictionary to match line 9 and also fixed formatting when printing out price
print(f"A {product['name']} costs ${total:.2f}")
