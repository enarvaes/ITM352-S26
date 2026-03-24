# Read a json file of taxi trip data and make a dataframe 
# Calculate the median fare
import json
import pandas as pd

taxi_df = pd.read_json("C:\\Users\\echan\\OneDrive\\Documents\\Github\\ITM352-S26\\ITM352-S26\\Lab10\\Taxi_Trips.json")
print(taxi_df.describe())

print ("Median fare is:", taxi_df.head(8))
median_fare = taxi_df["fare_amount"].median()
print("Median fare is:", median_fare)