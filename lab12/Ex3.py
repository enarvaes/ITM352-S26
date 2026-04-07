# Import libraries needed to open the URL, skip SSL errors, and parse HTML
import ssl
import urllib.request
from bs4 import BeautifulSoup

url = "https://shidler.hawaii.edu/itm/people"

# Skip SSL certificate checks so the website doesn't block us
ssl._create_default_https_context = ssl._create_unverified_context

# Open the webpage and parse its HTML with BeautifulSoup
print("Opening URL:", url)
web_page = urllib.request.urlopen(url)
html = web_page.read()
soup = BeautifulSoup(html, "html.parser")

# prettify() formats the HTML in a readable way — print just the first few lines
pretty_html = soup.prettify()
print("\nFirst few lines of the parsed HTML:")
for line in pretty_html.splitlines()[:10]:
    print(line)

# Find all h2 tags that link to an /itm/directory/ page — those are the people
# Use a set to avoid counting duplicates (some people appear in multiple sections)
people = []
seen = set()
for h2 in soup.find_all("h2"):
    a = h2.find("a", href=lambda href: href and "/itm/directory/" in href)
    if a:
        name = a.get_text(strip=True)
        if name not in seen:
            seen.add(name)
            people.append(name)

# Print each person and the total count
print("\nITM People:")
for person in people:
    print(" -", person)
print(f"\nTotal people found: {len(people)}")
