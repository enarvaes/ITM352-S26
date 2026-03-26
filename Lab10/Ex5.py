import pandas as pd

# Load the CSV file
df_homes = pd.read_csv("C:\\Users\\echan\\OneDrive\\Documents\\Github\\ITM352-S26\\ITM352-S26\\Lab10\\homes_data.csv")

# 1. Look at original data types
print("Original data types:")
print(df_homes.dtypes)

# 2. Coerce incorrect columns to numeric
cols_to_fix = ['land_sqft', 'gross_sqft', 'sale_price']

for col in cols_to_fix:
    df_homes[col] = pd.to_numeric(df_homes[col], errors='coerce')

# 3. Look at updated data types
print("\nCleaned data types:")
print(df_homes.dtypes)

# 4. Print cleaned data
print("\nCleaned data (first 10 rows):")
print(df_homes.head(10))

# Drop rows with any null values
df_homes_clean = df_homes.dropna()

# Drop duplicate rows
df_homes_clean = df_homes_clean.drop_duplicates()

# Print the cleaned results
print("Cleaned DataFrame (first 10 rows):")
print(df_homes_clean.head(10))

# Print updated shape
print("\nNew dimensions:", df_homes_clean.shape)

# Filter out 0 or missing sales
df_sales = df_homes_clean[df_homes_clean['sale_price'] > 0]

# Print results
print("Filtered sales data (first 10 rows):")
print(df_sales.head(10))

# Compute average sale price
average_sale_price = df_sales['sale_price'].mean()
print("\nAverage sale price:", average_sale_price)