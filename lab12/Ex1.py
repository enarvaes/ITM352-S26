# Scrape data from the city of Chicago data portal
# Print ant line that has a <title> tag in it

import urllib.request
import ssl

url = "https://data.cityofchicago.org/Historic-Preservation/Landmark-Districts/zidz-sdfj/about_data"
ssl._create_default_https_context = ssl._create_unverified_context

print("opening url: ", url)
web_page = urllib.request.urlopen(url)

# Interate through each line in the web page, searching for <title> tags
for line in web_page:
    line = line.decode("utf-8")  # Decode the line from bytes to a string
    if "<title>" in line:
        print(line.strip())  # Print the line with leading/trailing whitespace removed
