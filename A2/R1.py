import time
from pathlib import Path

import pandas as pd

# I keep the file path at the top so it is easy to change later.


LOCAL_SALES_FILE = Path(__file__).parent / "sales_data.csv"

# Fields required across the dashboard analytics.
REQUIRED_FIELDS = {
    "order_number",
    "employee_id",
    "sales_region",
    "order_date",
    "order_type",
    "customer_type",
    "product_category",
    "quantity",
    "unit_price",
}


def validate_required_fields(data):
    # Quick check so we can warn about missing columns before running analytics.
    missing = sorted(REQUIRED_FIELDS.difference(data.columns))
    if missing:
        print("WARNING: The dataset is missing required field(s):")
        print(missing)
        print("Some analytics may not work correctly.")
    else:
        print("All required fields for dashboard analytics are present.")


def load_csv(file_path):
    print("Loading sales data. Please wait...")
    print(f"Source: {file_path}")
    start_time = time.time()
    try:
        data = pd.read_csv(file_path)
        data = data.fillna(0)

        if {"quantity", "unit_price"}.issubset(data.columns):
            data["sales"] = data["quantity"] * data["unit_price"]

        if "order_date" in data.columns:
            data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce")
            data["order_date"] = data["order_date"].fillna(pd.Timestamp("1970-01-01"))

        validate_required_fields(data)

        elapsed = time.time() - start_time
        print("Sales data loaded successfully.")
        print(f"Load time: {elapsed:.2f} seconds")
        print(f"Rows: {len(data)}")
        print(f"Columns: {list(data.columns)}")
        return data
    except Exception as error:
        # If loading fails, stop with one clear message.
        raise SystemExit(f"ERROR: Failed to load sales data. {error}")


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


def sales_by_product_category_order_type(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    required = {"product_category", "order_type", "sales"}
    if not required.issubset(data.columns):
        print("Missing required columns: product_category, order_type, and/or sales.")
        return

    pivot = pd.pivot_table(
        data,
        index="product_category",
        columns="order_type",
        values="sales",
        aggfunc="sum",
        fill_value=0,
    )

    print("\nTotal sales by product category and order type:")
    print(pivot)


def average_sales_by_customer_type_region(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    required = {"customer_type", "sales_region", "sales"}
    if not required.issubset(data.columns):
        print("Missing required columns: customer_type, sales_region, and/or sales.")
        return

    pivot = pd.pivot_table(
        data,
        index="customer_type",
        columns="sales_region",
        values="sales",
        aggfunc="mean",
        fill_value=0,
    )

    print("\nAverage sales by customer type and region:")
    print(pivot)


def quantity_by_product_category_customer_type(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    required = {"product_category", "customer_type", "quantity"}
    if not required.issubset(data.columns):
        print("Missing required columns: product_category, customer_type, and/or quantity.")
        return

    pivot = pd.pivot_table(
        data,
        index="product_category",
        columns="customer_type",
        values="quantity",
        aggfunc="sum",
        fill_value=0,
    )

    print("\nTotal quantity by product category and customer type:")
    print(pivot)


def get_user_selection(options, prompt):
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    choice = input("Enter the number(s) of your choice(s), separated by commas: ").strip()
    selected = [options[int(i.strip()) - 1] for i in choice.split(",")] if choice else []
    return selected


def generate_custom_pivot_table(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    print("custom table")

    row_options = list(data.columns)
    col_options = row_options
    value_options = list(data.select_dtypes(include=["number"]).columns)
    agg_options = ["sum", "mean", "count"]

    rows = get_user_selection(row_options, "Select rows:")
    if not rows:
        print("Row selection is required.")
        return

    col_options = [col for col in col_options if col not in rows]
    cols = get_user_selection(col_options, "Select columns (optional):")
    values = get_user_selection(value_options, "Select value field(s):")
    if not values:
        print("Value selection is required.")
        return

    agg_func = get_user_selection(agg_options, "Select aggregation function(s):")
    if not agg_func:
        print("Aggregation function selection is required.")
        return

    try:
        pivot_table = pd.pivot_table(
            data,
            index=rows,
            columns=cols if cols else None,
            values=values,
            aggfunc=agg_func,
        )
        print("\nCustom pivot table:")
        print(pivot_table)
    except Exception as error:
        print(f"Could not generate custom pivot table: {error}")


def exit_program(data):
    print("Exiting program. Goodbye!")
    raise SystemExit(0)


def display_menu():
    # Each menu line points to a function, so changing the menu is easy.
    menu_options = (
        ("Show the first n rows of sales data", display_initial_rows),
        ("Show the number of employees by region", show_employees_by_region),
        ("Show total sales by product category and order type", sales_by_product_category_order_type),
        ("Show average sales by customer type and region", average_sales_by_customer_type_region),
        ("Show total quantity by product category and customer type", quantity_by_product_category_customer_type),
        ("Create custom pivot table", generate_custom_pivot_table),
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
    # Keep running until the user picks Exit.
    sales_data = load_csv(LOCAL_SALES_FILE)

    while True:
        choice, menu_options = display_menu()
        _, selected_function = menu_options[choice - 1]
        selected_function(sales_data)


if __name__ == "__main__":
    main()