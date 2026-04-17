"""
ex7.py
Task 7: Create a 3D plot of fare, trip miles, and dropoff area from Trips from area 8.json.
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


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

    try:
        df = load_json_dataframe(filepath)
    except FileNotFoundError as exc:
        print(exc)
    else:
        fare_col = find_column(df, ["fare", "Fare", "trip_fare"])
        miles_col = find_column(df, ["trip_miles", "Trip_Miles", "Trip Miles", "tripMiles"])
        dropoff_col = find_column(df, ["dropoff_community_area", "Dropoff_Community_Area", "dropoff_area", "dropoff_community_area"])
        if fare_col is None or miles_col is None or dropoff_col is None:
            print("Could not find fare, trip miles, or dropoff area columns in the JSON file.")
        else:
            df = df[[fare_col, miles_col, dropoff_col]].dropna()
            df[fare_col] = pd.to_numeric(df[fare_col], errors="coerce")
            df[miles_col] = pd.to_numeric(df[miles_col], errors="coerce")
            df = df.dropna()
            df["dropoff_code"], uniques = pd.factorize(df[dropoff_col].astype(str))

            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection="3d")
            scatter = ax.scatter(
                df[fare_col],
                df[miles_col],
                df["dropoff_code"],
                c=df["dropoff_code"],
                cmap="viridis",
                alpha=0.7,
                s=35,
            )
            ax.set_title("3D Plot: Fare, Trip Miles, Dropoff Area")
            ax.set_xlabel("Fare")
            ax.set_ylabel("Trip Miles")
            ax.set_zlabel("Dropoff Area Code")
            cbar = fig.colorbar(scatter, ax=ax, shrink=0.6, pad=0.1)
            cbar.set_label("Dropoff Area Category")
            plt.tight_layout()
            output_file = os.path.join(os.path.dirname(__file__), "ex7_3d_plot.png")
            plt.savefig(output_file)
            print(f"Saved 3D plot to {output_file}")
            plt.show()
