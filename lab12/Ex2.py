# Import the libraries we need to open websites, skip SSL errors, and work with tables
import ssl
import pandas as pd
import urllib.request
import lxml

# The URL of the Treasury page that has the interest rate table
url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202603"

# Skip SSL certificate checks so the website doesn't block us
ssl._create_default_https_context = ssl._create_unverified_context

# Open the webpage and pull all HTML tables into a list of DataFrames
print("Opening URL:", url)
web_page = urllib.request.urlopen(url)
data_frames = pd.read_html(web_page)

# Grab the first table and print its column names
interest_rate_table = data_frames[0]
print("\nColumns in the interest rate table:")
print(interest_rate_table.columns.tolist())

# Loop through each row and print the date along with the 1 month interest rate
print("\n1 Month Interest Rates:")
for index, row in interest_rate_table.iterrows():
    print(row['Date'], ":", row['1 Mo'])
