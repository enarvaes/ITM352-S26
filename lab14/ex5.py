"""
ex5.py
Task 5: Create several scatter plots of fare vs trip miles from Trips from area 8.json.
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
            df = df[[fare_col, miles_col]].dropna()
            df[fare_col] = pd.to_numeric(df[fare_col], errors="coerce")
            df[miles_col] = pd.to_numeric(df[miles_col], errors="coerce")
            df = df.dropna()

            plt.figure(figsize=(8, 6))
            plt.scatter(df[fare_col], df[miles_col], alpha=0.6)
            plt.title("Fare vs Trip Miles (plt.scatter)")
            plt.xlabel("Fare")
            plt.ylabel("Trip Miles")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            output_file1 = os.path.join(os.path.dirname(__file__), "ex5_fare_vs_miles_scatter.png")
            plt.savefig(output_file1)
            print(f"Saved first scatter plot to {output_file1}")
            plt.show()

            plt.figure(figsize=(8, 6))
            plt.plot(df[fare_col], df[miles_col], linestyle="none", marker=".")
            plt.title("Fare vs Trip Miles (plt.plot with marker='.')")
            plt.xlabel("Fare")
            plt.ylabel("Trip Miles")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            output_file2 = os.path.join(os.path.dirname(__file__), "ex5_fare_vs_miles_plot.png")
            plt.savefig(output_file2)
            print(f"Saved second plot to {output_file2}")
            plt.show()

            plt.figure(figsize=(8, 6))
            plt.plot(
                df[fare_col],
                df[miles_col],
                linestyle="none",
                marker="v",
                color="cyan",
                alpha=0.2,
            )
            plt.title("Fare vs Trip Miles (fancy style)")
            plt.xlabel("Fare")
            plt.ylabel("Trip Miles")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            output_file3 = os.path.join(os.path.dirname(__file__), "ex5_fare_vs_miles_fancy.png")
            plt.savefig(output_file3)
            print(f"Saved fancy plot to {output_file3}")
            plt.show()
