"""
ex4.py
Task 4: Create a scatter plot of fare vs tip from Trips_Fri07072017T4 trip_miles gt1.json.
"""

import os
import matplotlib.pyplot as plt
import pandas as pd


def load_dataframe(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    if filepath.endswith('.json'):
        try:
            return pd.read_json(filepath)
        except ValueError:
            return pd.read_json(filepath, lines=True)
    elif filepath.endswith('.csv'):
        return pd.read_csv(filepath)
    else:
        raise ValueError("Unsupported file format")


def find_column(df, candidates):
    for name in candidates:
        if name in df.columns:
            return name
    return None


if __name__ == "__main__":
    filepath = os.path.join(os.path.dirname(__file__), "taxi trips Fri 7_7_2017.csv")  # Using CSV file that has tips

    try:
        df = load_dataframe(filepath)
    except FileNotFoundError as exc:
        print(exc)
    else:
        fare_col = find_column(df, ["fare", "Fare", "total_fare", "trip_fare"])
        tip_col = find_column(df, ["tip", "Tip", "tips", "Tips"])
        if fare_col is None or tip_col is None:
            print("Could not find fare or tip columns in the file.")
            print("Available columns:", list(df.columns))
        else:
            df = df[[fare_col, tip_col]].dropna()
            df[fare_col] = pd.to_numeric(df[fare_col], errors="coerce")
            df[tip_col] = pd.to_numeric(df[tip_col], errors="coerce")
            df = df.dropna()
            plt.figure(figsize=(8, 6))
            plt.scatter(df[fare_col], df[tip_col], alpha=0.65, edgecolors="w", linewidths=0.5)
            plt.title("Scatter Plot of Fare vs Tip")
            plt.xlabel("Fare")
            plt.ylabel("Tip")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            output_file = os.path.join(os.path.dirname(__file__), "ex4_fare_vs_tip.png")
            plt.savefig(output_file)
            print(f"Saved scatter plot to {output_file}")
            plt.show()
