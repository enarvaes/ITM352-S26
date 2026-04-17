"""
ex3.py
Task 3: Create a histogram of payment method vs sum of tips from Trips from area 8.json.
"""

import os
import matplotlib.pyplot as plt
import pandas as pd


def load_json_dataframe(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    try:
        return pd.read_json(filepath)
    except ValueError:
        return pd.read_json(filepath, lines=True)


def find_column(df, candidates):
    lowered = {col.lower(): col for col in df.columns}
    for name in candidates:
        key = name.lower()
        if key in lowered:
            return lowered[key]
    for name in candidates:
        key = name.lower()
        for col_lower, original in lowered.items():
            if key in col_lower or col_lower in key:
                return original
    return None


if __name__ == "__main__":
    filepath = os.path.join(os.path.dirname(__file__), "Trips from area 8.json")

    try:
        df = load_json_dataframe(filepath)
    except FileNotFoundError as exc:
        print(exc)
    else:
        payment_col = find_column(
            df,
            [
                "payment_method",
                "Payment_Method",
                "payment method",
                "Payment Type",
                "payment",
                "paymenttype",
                "payment_type",
            ],
        )
        tip_col = find_column(
            df,
            [
                "tip",
                "Tip",
                "tips",
                "Tips",
                "tip_amount",
                "tipamount",
            ],
        )
        if payment_col is None or tip_col is None:
            print("Could not find payment method or tip columns in the JSON file.")
            print("Available columns:", list(df.columns))
        else:
            grouped = (
                df[[payment_col, tip_col]]
                .dropna()
                .assign(**{tip_col: pd.to_numeric(df[tip_col], errors="coerce")})
            )
            grouped = grouped.dropna(subset=[tip_col])
            totals = grouped.groupby(payment_col)[tip_col].sum().sort_values(ascending=False)
            plt.figure(figsize=(10, 6))
            totals.plot(kind="bar", color="#5c9edc", edgecolor="black")
            plt.title("Total Tips by Payment Method")
            plt.xlabel("Payment Method")
            plt.ylabel("Total Tips")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            output_file = os.path.join(os.path.dirname(__file__), "ex3_tips_by_payment.png")
            plt.savefig(output_file)
            print(f"Saved plot to {output_file}")
            plt.show()
