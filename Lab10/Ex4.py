# Read a json file of taxi trip data and make a dataframe 
# Calculate the median fare
import json
import pandas as pd

taxi_df = pd.read_json("C:\\Users\\echan\\OneDrive\\Documents\\Github\\ITM352-S26\\ITM352-S26\\Lab10\\Taxi_Trips.json")

print(taxi_df.describe())

# Print first 8 rows (optional)
print("First 8 rows:")
print(taxi_df.head(8))

# Correct column name is 'fare'
median_fare = taxi_df['fare'].median()
print("Median fare is:", median_fare)