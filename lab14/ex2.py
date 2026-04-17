"""
ex2.py
Task 2: Create a histogram of trip miles from Trips from area 8.json.
"""

import json
import os
import matplotlib.pyplot as plt
import pandas as pd


def load_json_dataframe(filepath):
    """Load JSON file into a pandas DataFrame with robust handling."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    try:
        return pd.read_json(filepath)
    except ValueError:
        return pd.read_json(filepath, lines=True)


def find_column(df, candidates):
    """Return the first column name in df that matches any of the candidate names."""
    for name in candidates:
        if name in df.columns:
            return name
    return None


if __name__ == "__main__":
    filepath = os.path.join(os.path.dirname(__file__), "Trips from area 8.json")

    try:
        df = load_json_dataframe(filepath)
    except FileNotFoundError as exc:
        print(exc)
    else:
        trip_miles_col = find_column(df, ["trip_miles", "Trip_Miles", "Trip Miles", "tripMiles"])
        if trip_miles_col is None:
            print("Could not find a trip miles column in the JSON file.")
            print("Available columns:", list(df.columns))
        else:
            trip_miles = pd.to_numeric(df[trip_miles_col], errors="coerce").dropna()
            plt.figure(figsize=(8, 6))
            plt.hist(trip_miles, bins=15, edgecolor="black")
            plt.title("Histogram of Trip Miles")
            plt.xlabel("Trip Miles")
            plt.ylabel("Frequency")
            plt.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            output_file = os.path.join(os.path.dirname(__file__), "ex2_trip_miles_histogram.png")
            plt.savefig(output_file)
            print(f"Saved histogram to {output_file}")
            plt.show()
