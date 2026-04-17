"""
ex8.py
On Your Own: Create a heatmap from pickup_community_area and dropoff_community_area.
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def find_column(df, candidates):
    """Return the first column name in df that matches any of the candidate names."""
    for name in candidates:
        if name in df.columns:
            return name
    return None


if __name__ == "__main__":
    filepath = os.path.join(os.path.dirname(__file__), "taxi trips Fri 7_7_2017.csv")

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
    else:
        df = pd.read_csv(filepath)
        pickup_candidates = ["pickup_community_area", "Pickup Community Area"]
        dropoff_candidates = ["dropoff_community_area", "Dropoff Community Area"]
        pickup_col = find_column(df, pickup_candidates)
        dropoff_col = find_column(df, dropoff_candidates)

        if pickup_col is None or dropoff_col is None:
            print("The expected columns are not present in the CSV file.")
            print("Available columns:", list(df.columns))
        else:
            heatmap_data = (
                df.dropna(subset=[pickup_col, dropoff_col])
                .groupby([pickup_col, dropoff_col])
                .size()
                .unstack(fill_value=0)
            )
            plt.figure(figsize=(12, 10))
            sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=0.5)
            plt.title("Pickup Area vs Dropoff Area Heatmap")
            plt.xlabel("Dropoff Community Area")
            plt.ylabel("Pickup Community Area")
            plt.tight_layout()
            output_file = os.path.join(os.path.dirname(__file__), "ex8_heatmap.png")
            plt.savefig(output_file)
            print(f"Saved heatmap to {output_file}")
            plt.show()
