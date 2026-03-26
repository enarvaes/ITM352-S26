import numpy as np

hh_income = [
    (10, 14629),
    (20, 25600),
    (30, 37002),
    (40, 50000),
    (50, 63179),
    (60, 79542),
    (70, 100162),
    (80, 130000),
    (90, 184292)
]

hh_income_array = np.array(hh_income)

# Report the dimensions and number of elements
print("Dimensions of the array:", hh_income_array.ndim)
print("Shape of the array:", hh_income_array.shape)
print("Number of elements in the array:", hh_income_array.size)

# Print table header
print("\nPercentile   Household Income")
print("-" * 30)

# Print each row in a formatted table
for percentile, income in hh_income_array:
    print(f"{percentile:>9}%   ${income:>10,}")
