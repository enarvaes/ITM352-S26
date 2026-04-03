# Read in a file from a URL and save a local CSV file with the first 10 rows

import time
from pathlib import Path

import pandas as pd
import numpy as np
import pyarrow



def lload_csv(file_path):
    print(f"Loading file: {file_path}")
    start_time = time.time()
    try:
        df = pd.read_csv(file_path, engine="pyarrow")
        end_time = time.time()
        load_time = end_time - start_time
        print(f"File loaded successfully in {load_time:.2f} seconds.")
        print(f"Number of rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        required_columns = ['quantity', 'unit_price', 'order_date']

        #Check if required columns are present
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Warning: Missing columns in the dataset: {missing_columns}")
        else:
            print("All required columns are present.")


        return df
        
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return None

# Call load_csv to load the data and print the first 10 rows
#filename = 'https://drive.google.com/uc?id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA&export=download'
filename = Path(__file__).parent / "sales_data_test.csv"
sales_data = lload_csv(filename)

if sales_data is not None:
    print(sales_data.head(10))


