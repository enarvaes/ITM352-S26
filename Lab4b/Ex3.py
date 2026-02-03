url = input("Enter a full URL: ")

cleaned_url = url.replace("https://", "")

print(f"Cleaned URL: {cleaned_url}")

parts = cleaned_url.split(".")

domain = parts[1]
print(f"Domain: {domain}")

top_level_domain = parts[2]
print(f"Top-Level Domain: {top_level_domain.strip('/')}")
