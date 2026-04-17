"""
ex1.py
Task 1: Create a first simple visualization using matplotlib.
"""

import matplotlib.pyplot as plt
import os

# Define two sets of data points with the same length
x_values = [1, 2, 3, 4, 5]
y_values = [2, 4, 1, 3, 5]

# Second dataset to plot on the same axes
x_values2 = [1, 2, 3, 4, 5]
y_values2 = [1, 3, 2, 5, 4]

plt.figure(figsize=(8, 6))
# Plot the first dataset as a line graph
plt.plot(x_values, y_values, label='Line 1', color='blue')
# Plot the first dataset again as scatter points
plt.scatter(x_values, y_values, label='Scatter 1', color='red')
# Add a second line graph using the second dataset
plt.plot(x_values2, y_values2, label='Line 2', color='green', linestyle='--')

# Add labels and title
plt.title('Simple matplotlib Visualization')
plt.xlabel('X values')
plt.ylabel('Y values')
plt.legend()
plt.grid(True)
plt.tight_layout()
output_file = os.path.join(os.path.dirname(__file__), "ex1_simple_viz.png")
plt.savefig(output_file)
print(f"Saved visualization to {output_file}")
plt.show()
