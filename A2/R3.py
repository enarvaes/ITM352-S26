import time
from pathlib import Path

import pandas as pd

# CSV location for the dashboard.


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
    # Warn if we are missing columns used by analytics.
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
        raise SystemExit(f"ERROR: Failed to load sales data. {error}")


def display_initial_rows(data):
    if data is None or data.empty:
        print("No data available.")
        return

    while True:
        # Print choices so user knows what to type.
        print("\nEnter rows to display:")
        print(f"- Enter a number 1 to {len(data)}")
        print("- To see all rows, enter 'all'")
        print("- To skip preview, press Enter")
        user_input = input("Your choice: ").strip().lower()

        if user_input == "":
            print("Preview skipped.")
            return

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

    required = {"sales_region", "order_type", "sales"}
    if not required.issubset(data.columns):
        print("Missing required columns: sales_region, order_type, and/or sales.")
        return

    pivot = pd.pivot_table(
        data,
        index="sales_region",
        columns="order_type",
        values="sales",
        aggfunc="sum",
        fill_value=0,
    )

    print("\nTotal sales by region and order type:")
    print(pivot)


def average_sales_by_region_with_state_sale_type(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    required = {"sales_region", "customer_state", "order_type", "sales"}
    if not required.issubset(data.columns):
        print("Missing required columns: sales_region, customer_state, order_type, and/or sales.")
        return

    pivot = pd.pivot_table(
        data,
        index="sales_region",
        columns=["customer_state", "order_type"],
        values="sales",
        aggfunc="mean",
        fill_value=0,
    )
    print("\nAverage sales by region with average sales by state and sale type:")
    print(pivot)


def sales_by_customer_type_order_type_by_state(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    required = {"customer_state", "customer_type", "order_type", "sales"}
    if not required.issubset(data.columns):
        print("Missing required columns: customer_state, customer_type, order_type, and/or sales.")
        return

    pivot = pd.pivot_table(
        data,
        index=["customer_state", "customer_type"],
        columns="order_type",
        values="sales",
        aggfunc="sum",
        fill_value=0,
    )

    print("\nSales by customer type and order type by state:")
    print(pivot)


def total_sales_quantity_and_price_by_region_and_product(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    required = {"sales_region", "product_category", "quantity", "sales"}
    if not required.issubset(data.columns):
        print("Missing required columns: sales_region, product_category, quantity, and/or sales.")
        return

    pivot = pd.pivot_table(
        data,
        index=["sales_region", "product_category"],
        values=["quantity", "sales"],
        aggfunc="sum",
        fill_value=0,
    )

    print("\nTotal sales quantity and price by region and product:")
    print(pivot)


def total_sales_quantity_and_price_by_customer_type(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    required = {"order_type", "customer_type", "quantity", "sales"}
    if not required.issubset(data.columns):
        print("Missing required columns: order_type, customer_type, quantity, and/or sales.")
        return

    pivot = pd.pivot_table(
        data,
        index=["order_type", "customer_type"],
        values=["quantity", "sales"],
        aggfunc="sum",
        fill_value=0,
    )

    print("\nTotal sales quantity and price by customer type:")
    print(pivot)


def max_min_sales_price_by_category(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    required = {"product_category", "unit_price"}
    if not required.issubset(data.columns):
        print("Missing required columns: product_category and/or unit_price.")
        return

    pivot = pd.pivot_table(
        data,
        index="product_category",
        values="unit_price",
        aggfunc=["max", "min"],
        fill_value=0,
    )

    print("\nMax and min sales price by category:")
    print(pivot)


def unique_employees_by_region(data):
    if data is None or data.empty:
        print("No data available to summarize.")
        return

    required = {"sales_region", "employee_id"}
    if not required.issubset(data.columns):
        print("Missing required columns: sales_region and/or employee_id.")
        return

    pivot = pd.pivot_table(
        data,
        index="sales_region",
        values="employee_id",
        aggfunc="nunique",
        fill_value=0,
    )

    print("\nNumber of unique employees by region:")
    print(pivot)


def get_user_selection(options, prompt):
    # Keep asking until the user enters valid option numbers.
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    while True:
        choice = input("Enter the number(s) of your choice(s), separated by commas: ").strip()
        if not choice:
            return []
        try:
            selected = []
            for item in choice.split(","):
                index = int(item.strip()) - 1
                if not 0 <= index < len(options):
                    raise ValueError
                selected.append(options[index])
            return selected
        except ValueError:
            print("Invalid selection. Please try again.")


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
    # Easy to edit menu: each item is (text, function).
    menu_options = (
        ("Show the first n rows of sales data", display_initial_rows),
        ("Total sales by region and order_type", sales_by_region_order_type),
        ("Average sales by region with average sales by state and sale type", average_sales_by_region_with_state_sale_type),
        ("Sales by customer type and order type by state", sales_by_customer_type_order_type_by_state),
        ("Total sales quantity and price by region and product", total_sales_quantity_and_price_by_region_and_product),
        ("Total sales quantity and price customer type", total_sales_quantity_and_price_by_customer_type),
        ("Max and min sales price of sales by category", max_min_sales_price_by_category),
        ("Number of unique employees by region", unique_employees_by_region),
        ("Create custom pivot table", generate_custom_pivot_table),
        ("Exit the program", exit_program),
    )

    while True:
        print("\n--- Sales Data Dashboard ---")
        for i, (text, _) in enumerate(menu_options, start=1):
            print(f"{i}. {text}")

        user_input = input(f"Enter your choice (1-{len(menu_options)}): ").strip()
        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(menu_options):
                return choice, menu_options

        print("Invalid selection. Please try again.")


def main():
    sales_data = load_csv(LOCAL_SALES_FILE)

    while True:
        choice, menu_options = display_menu()
        _, selected_function = menu_options[choice - 1]
        selected_function(sales_data)


if __name__ == "__main__":
    main()