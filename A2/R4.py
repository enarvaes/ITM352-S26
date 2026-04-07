import time
from pathlib import Path

import pandas as pd

# Path to the local data file.


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
    assert isinstance(data, pd.DataFrame), "validate_required_fields expects a pandas DataFrame"
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


def require_columns(data, required_columns, context_name):
    """Validate required columns for an analysis step and fail gracefully."""
    # One shared column check keeps behavior consistent.
    assert isinstance(data, pd.DataFrame), f"{context_name} expects a pandas DataFrame"
    missing = sorted(set(required_columns).difference(data.columns))
    if missing:
        print(f"Missing required columns for {context_name}: {missing}")
        return False
    return True


def build_pivot_table(data, index, columns, values, aggfunc, title):
    """Create and print a pivot table safely so all analytics share one code path."""
    # Shared pivot helper so all reports print the same way.
    try:
        pivot = pd.pivot_table(
            data,
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc,
            fill_value=0,
        )
        print(f"\n{title}")
        print(pivot)
        return pivot
    except Exception as error:
        print(f"Could not generate pivot table for {title}: {error}")
        return None


def display_initial_rows(data):
    if data is None or data.empty:
        print("No data available.")
        return

    while True:
        print("\nEnter rows to display:")
        print(f"- Enter a number 1 to {len(data)}")
        print("- To see all rows, enter 'all'")
        print("- To skip preview, press Enter")
        user_input = input("Your choice: ").strip().lower()

        if user_input == "":
            print("Preview skipped.")
            return None

        if user_input == "all":
            print(data)
            return data

        if user_input.isdigit():
            n = int(user_input)
            if 1 <= n <= len(data):
                result = data.head(n)
                print(result)
                return result

        print("Invalid input. Please enter a valid number or 'all'.")


def sales_by_region_order_type(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    if not require_columns(data, {"sales_region", "order_type", "sales"}, "sales_by_region_order_type"):
        return

    return build_pivot_table(
        data=data,
        index="sales_region",
        columns="order_type",
        values="sales",
        aggfunc="sum",
        title="Total sales by region and order type:",
    )


def average_sales_by_region_with_state_sale_type(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    if not require_columns(
        data,
        {"sales_region", "customer_state", "order_type", "sales"},
        "average_sales_by_region_with_state_sale_type",
    ):
        return

    return build_pivot_table(
        data=data,
        index="sales_region",
        columns=["customer_state", "order_type"],
        values="sales",
        aggfunc="mean",
        title="Average sales by region with average sales by state and sale type:",
    )


def sales_by_customer_type_order_type_by_state(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    if not require_columns(
        data,
        {"customer_state", "customer_type", "order_type", "sales"},
        "sales_by_customer_type_order_type_by_state",
    ):
        return

    return build_pivot_table(
        data=data,
        index=["customer_state", "customer_type"],
        columns="order_type",
        values="sales",
        aggfunc="sum",
        title="Sales by customer type and order type by state:",
    )


def total_sales_quantity_and_price_by_region_and_product(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    if not require_columns(
        data,
        {"sales_region", "product_category", "quantity", "sales"},
        "total_sales_quantity_and_price_by_region_and_product",
    ):
        return

    return build_pivot_table(
        data=data,
        index=["sales_region", "product_category"],
        columns=None,
        values=["quantity", "sales"],
        aggfunc="sum",
        title="Total sales quantity and price by region and product:",
    )


def total_sales_quantity_and_price_by_customer_type(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    if not require_columns(
        data,
        {"order_type", "customer_type", "quantity", "sales"},
        "total_sales_quantity_and_price_by_customer_type",
    ):
        return

    return build_pivot_table(
        data=data,
        index=["order_type", "customer_type"],
        columns=None,
        values=["quantity", "sales"],
        aggfunc="sum",
        title="Total sales quantity and price by customer type:",
    )


def max_min_sales_price_by_category(data):
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    if not require_columns(data, {"product_category", "unit_price"}, "max_min_sales_price_by_category"):
        return

    return build_pivot_table(
        data=data,
        index="product_category",
        columns=None,
        values="unit_price",
        aggfunc=["max", "min"],
        title="Max and min sales price by category:",
    )


def unique_employees_by_region(data):
    if data is None or data.empty:
        print("No data available to summarize.")
        return

    if not require_columns(data, {"sales_region", "employee_id"}, "unique_employees_by_region"):
        return

    return build_pivot_table(
        data=data,
        index="sales_region",
        columns=None,
        values="employee_id",
        aggfunc="nunique",
        title="Number of unique employees by region:",
    )


def get_user_selection(options, prompt, allow_empty=False):
    """Return selected option values from a numbered list with full input validation."""
    assert isinstance(options, list), "options must be a list"
    assert len(options) > 0, "options list must not be empty"

    print(prompt)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")

    input_prompt = "Enter the number(s) of your choice(s), separated by commas: "
    if allow_empty:
        input_prompt = "Enter the number(s) of your choice(s), separated by commas (Enter for no grouping): "

    while True:
        # Keep asking until input is valid.
        choice = input(input_prompt).strip()
        if not choice:
            if allow_empty:
                return []
            print("At least one selection is required.")
            continue

        try:
            selected = []
            seen = set()
            for item in choice.split(","):
                index = int(item.strip()) - 1
                if not 0 <= index < len(options):
                    raise ValueError

                value = options[index]
                if value not in seen:
                    selected.append(value)
                    seen.add(value)
            return selected
        except ValueError:
            print("Invalid selection. Please try again.")


def generate_custom_pivot_table(data):
    """Interactive Pivot Table Generator for user-defined ad-hoc analysis."""
    if data is None or data.empty:
        print("No data available to analyze.")
        return

    assert isinstance(data, pd.DataFrame), "generate_custom_pivot_table expects a DataFrame"

    print("\n--- Pivot Table Generator ---")
    print("Build your own pivot table by selecting rows, optional columns, values, and aggregation.")

    # Options come from real columns in the loaded data.
    row_options = list(data.columns)
    col_options = list(row_options)
    value_options = list(data.select_dtypes(include=["number"]).columns)
    agg_options = ["sum", "mean", "count"]

    if not value_options:
        print("No numeric columns are available for values.")
        return

    rows = get_user_selection(row_options, "Select rows:")
    if not rows:
        print("Row selection is required.")
        return

    col_options = [col for col in col_options if col not in rows]
    cols = []
    if col_options:
        cols = get_user_selection(col_options, "Select columns (optional):", allow_empty=True)

    values = get_user_selection(value_options, "Select values:")
    if not values:
        print("Value selection is required.")
        return

    agg_func = get_user_selection(agg_options, "Select aggregation function:")
    if not agg_func:
        print("Aggregation function selection is required.")
        return

    return build_pivot_table(
        data=data,
        index=rows,
        columns=cols if cols else None,
        values=values,
        aggfunc=agg_func,
        title="Custom pivot table:",
    )


def exit_program(data):
    print("Exiting program. Goodbye!")
    raise SystemExit(0)


def display_menu():
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