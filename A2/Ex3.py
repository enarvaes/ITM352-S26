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
        df['order_date'] = pd.to_datetime(df['order_date'], format='%Y-%m-%d', errors='coerce')
        #df.fillna(0, inplace=True)  # Fill NaN values with 0 for numeric columns
        df['sales'] = df['quantity'] * df['unit_price']

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

def display_initial_rows(dataframe):
    print("Enter rows to display:")
    print(f" - Enter a number 1 to {len(dataframe)}")
    print(" - Enter 'all' to display all rows")
    print(" - to skip preview, press enter")
    user_input = input("Your choice: ").strip().lower()

    if user_input == "":
        print("Skipping preview.")
        return
    elif user_input == "all":
        print("Displaying all rows:")
        print(dataframe)
    elif user_input.isdigit():
        print(f"Displaying first {user_input} rows:")
        print(dataframe.head(int(user_input)))
    else:
        print("Invalid input. Please enter a valid number, 'all', or press enter to skip.")

def display_employees_by_region(dataframe):
    if dataframe is None or dataframe.empty:
        print("No data available to summarize.")
        return
    if "sales_region" not in dataframe.columns or "employee_id" not in dataframe.columns:
        print("Missing required columns: 'sales_region' and/or 'employee_id'.")
        return

    counts = dataframe.groupby("sales_region")["employee_id"].nunique().sort_values(ascending=False)
    print("Number of employees by region:")
    print(counts)

def exit_program(dataframe):
    print("Exiting the program. Goodbye!")
    exit(0)

def display_menu():
    menu_options = [
        ("show the first n rows of the data", display_initial_rows),
        ("show number of employees by region", display_employees_by_region),
        ("exit", exit_program),
    ]

    print("Available options:")
    for i, (option_text, _) in enumerate(menu_options, start=1):
        print(f"{i}. {option_text}")
    
    try:
        menu_len = len(menu_options)
        choice = int(input(f"Enter your choice: (1-{menu_len})"))
        if 1 <= choice <= menu_len:
            _, action = menu_options[choice - 1]
            action(sales_data)
        else:
            print("Invalid choice. Please select a valid option.")

    except ValueError:
        print("Invalid input. Please enter a number corresponding to the menu options.")



# Call load_csv to load the data and print the first 10 rows
#filename = 'https://drive.google.com/uc?id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA&export=download'
filename = Path(__file__).parent / "sales_data_test.csv"
sales_data = lload_csv(filename)


# Run the main processing loop
if sales_data is not None:
    print(sales_data.head(10))

    def main():
        while True:
            print ("Sales Data Dashboard")
            display_initial_rows(dataframe=sales_data)
            display_menu()

    if __name__ == "__main__":
        main()