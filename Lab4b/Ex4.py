#parsae through the portions of an email address
email = input("Enter your email address: ")

#method 1: using split function
parts = email.split("@")
username = parts[0]
domain = parts[1]

print(f"Username: {username}")
print(f"Domain: {domain}")

#method 2: using index function
at_symbol_index = email.index("@")
username_manual = email[:at_symbol_index]
domain_manual = email[at_symbol_index + 1:]
print(f"Username (manual): {username_manual}")
print(f"Domain (manual): {domain_manual}")
