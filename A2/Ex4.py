import time
from pathlib import Path

import pandas as pd


def load_csv(file_path):
    print(f"Loading file: {file_path}")
    start_time = time.time()
    try:
        data = pd.read_csv(file_path)
        data["order_date"] = pd.to_datetime(data["order_date"], format="%Y-%m-%d", errors="coerce")
        data["sales"] = data["quantity"] * data["unit_price"]

        elapsed = time.time() - start_time
        print(f"File loaded successfully in {elapsed:.2f} seconds.")
        print(f"Rows: {len(data)}")
        print(f"Columns: {list(data.columns)}")
        return data
    except Exception as error:
        print(f"An error occurred while loading the file: {error}")
        return None


def display_initial_rows(data):
    if data is None or data.empty:
        print("No data available.")
        return

    while True:
        user_input = input(f"Enter number of rows to display (1-{len(data)}) or 'all': ").strip().lower()

        if user_input == "all":
            print(data)
            return

        if user_input.isdigit():
            n = int(user_input)
            if 1 <= n <= len(data):
                print(data.head(n))
                return

        print("Invalid input. Please enter a valid number or 'all'.")


def sales_by_region_order_type(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    required = {"sales_region", "order_type", "employee_id"}
    if not required.issubset(data.columns):
        print("Missing required columns: sales_region, order_type, and/or employee_id.")
        return

    pivot = pd.pivot_table(
        data,
        index="sales_region",
        columns="order_type",
        values="employee_id",
        aggfunc="nunique",
        fill_value=0,
    )

    print("\nUnique employees by sales region and order type:")
    print(pivot)


def show_employees_by_region(data):
    if data is None or data.empty:
        print("No data available to summarize.")
        return

    required = {"sales_region", "employee_id"}
    if not required.issubset(data.columns):
        print("Missing required columns: sales_region and/or employee_id.")
        return

    counts = data.groupby("sales_region")["employee_id"].nunique().sort_values(ascending=False)
    print("\nNumber of unique employees by region:")
    print(counts)

    sales_by_region_order_type(data)


def exit_program(data):
    print("Exiting program. Goodbye!")
    raise SystemExit(0)


def display_menu():
    menu_options = (
        ("Show the first n rows of sales data", display_initial_rows),
        ("Show the number of employees by region", show_employees_by_region),
        ("Exit the program", exit_program),
    )

    while True:
        print("\n--- Sales Data Menu ---")
        for i, (text, _) in enumerate(menu_options, start=1):
            print(f"{i}. {text}")

        user_input = input(f"Enter your choice (1-{len(menu_options)}): ").strip()
        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(menu_options):
                return choice, menu_options

        print("Invalid selection. Please try again.")


def main():
    filename = Path(__file__).parent / "sales_data_test.csv"
    sales_data = load_csv(filename)

    if sales_data is None:
        return

    while True:
        choice, menu_options = display_menu()
        _, selected_function = menu_options[choice - 1]
        selected_function(sales_data)


if __name__ == "__main__":
    main()