"""
ex6.py
Task 6: Create a filtered scatter plot of fare vs trip miles and save it to FaresXmiles.png.
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
    for name in candidates:
        if name in df.columns:
            return name
    return None


if __name__ == "__main__":
    filepath = os.path.join(os.path.dirname(__file__), "Trips from area 8.json")
    output_file = os.path.join(os.path.dirname(__file__), "FaresXmiles.png")

    try:
        df = load_json_dataframe(filepath)
    except FileNotFoundError as exc:
        print(exc)
    else:
        fare_col = find_column(df, ["fare", "Fare", "trip_fare"])
        miles_col = find_column(df, ["trip_miles", "Trip_Miles", "Trip Miles", "tripMiles"])
        if fare_col is None or miles_col is None:
            print("Could not find fare or trip miles columns in the JSON file.")
        else:
            df = df[[fare_col, miles_col]].copy()
            df[fare_col] = pd.to_numeric(df[fare_col], errors="coerce")
            df[miles_col] = pd.to_numeric(df[miles_col], errors="coerce")
            df = df.dropna()
            df = df[df[miles_col] > 0]
            df = df[df[miles_col] >= 2]

            plt.figure(figsize=(8, 6))
            plt.scatter(df[fare_col], df[miles_col], s=15, alpha=0.6, color="teal")
            plt.title("Filtered Fare vs Trip Miles (>= 2 miles)")
            plt.xlabel("Fare")
            plt.ylabel("Trip Miles")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(output_file)
            plt.show()
            print(f"Saved filtered plot to {output_file}")
