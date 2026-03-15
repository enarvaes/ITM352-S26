import csv
import os

# Get the directory where this script is located for robust file access
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, "my_custom_spreadsheet.csv")

# Load the CSV file and extract Annual_Salary values
salaries = []
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        # Convert Annual_Salary to float and add to list
        salaries.append(float(row['Annual_Salary']))

# Calculate average, maximum, and minimum
if salaries:
    average_salary = sum(salaries) / len(salaries)
    max_salary = max(salaries)
    min_salary = min(salaries)

    print(f"Average Annual Salary: ${average_salary:.2f}")
    print(f"Maximum Annual Salary: ${max_salary:.2f}")
    print(f"Minimum Annual Salary: ${min_salary:.2f}")
else:
    print("No salary data found.")