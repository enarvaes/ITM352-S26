import requests
import pandas as pd

# Socrata query: count licenses grouped by driver_type
url = "https://data.cityofchicago.org/resource/97wa-y6ff.json?$select=driver_type,count(license)&$group=driver_type"

response = requests.get(url, timeout=30)
response.raise_for_status()

records = response.json()

print("Response records:")
print(records)
print("\nData format:", type(records), "with item type", type(records[0]) if records else "No items")

df = pd.DataFrame.from_records(records)[["count_license", "driver_type"]]
df.columns = ["count", "driver_type"]
df = df.set_index("driver_type")

print("\nDataFrame grouped by driver_type:")
print(df)
