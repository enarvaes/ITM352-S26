# Import sodapy to talk to Chicago's open data API and pandas to work with the data
from sodapy import Socrata
import pandas as pd

# Connect to Chicago's open data portal (no auth token needed for public data)
client = Socrata("data.cityofchicago.org", None)

# Fetch the first 500 records from the passenger vehicle license dataset
json_file = client.get("rr23-ymwb", limit=500)

df = pd.DataFrame.from_records(json_file)

print(df.head())

# Group vehicles by fuel source and print how many are in each group
fuel_counts = df["vehicle_fuel_source"].fillna("Unknown").value_counts()
print("\nNumber of vehicles per fuel source:")
print(fuel_counts)
