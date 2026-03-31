import pandas as pd
import numpy as np

filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

pd.set_option('display.max_columns', None)  # Show all columns in the output
pd.set_option('display.float_format', "${:,.2f}".format)

df = pd.read_csv(filename, engine='pyarrow')
df['order_date'] = pd.to_datetime(df['order_date'], format='%Y-%m-%d', errors='coerce')

df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
df['sales'] = df['quantity'] * df['unit_price']

# `pivot_table` expects index as column label, not the full Series object.
# Use string key 'customer_state' (or any column name) for cleaner semantics.

pivot_table = df.pivot_table(values='sales', index='customer_state',
                             columns='order_type',
                             aggfunc=['sum', 'mean'],
                             margins=True,
                             fill_value=0)
print(pivot_table)