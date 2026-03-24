# Create a list of tuples that are percentiles of household incomes
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

# Report rhe dimensions of the array and the number of eleements in the array
print("Dimensions of the array:", hh_income_array.ndim)
print("Dimensions v2:", hh_income_array.shape)
print("Number of elements in the array:", hh_income_array.size)

