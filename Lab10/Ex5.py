# Bring in a CVS file of some data and create a datafram
# Do some filtering and statistics on the data
import pandas as pd

df_homes = pd.read_csv("C:\\Users\\echan\\OneDrive\\Documents\\Github\\ITM352-S26\\ITM352-S26\\Lab10\\homes_data.csv")

# Pint out the shape of the dataframe and the first few rows

shape = df_homes.shape
print(f"The homes data has {shape[0]} rows and {shape[1]} columns.")
print(df_homes.head())

# Select on th properties with 500 or more units
df_big_homes = df_homes[df_homes['sq__ft'] >= 500]
df_big_properties = df_big_homes[['id', 'assessment']]
print(df_big_homes.head())