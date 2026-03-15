import csv
import os

# Get the directory where this script is located for robust file access
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, "taxi_1000.csv")

# Initialize variables for calculations
total_fare = 0.0
fare_count = 0
max_trip_miles = 0.0

# Read the CSV file
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        # Process Fare and Trip Miles only for fares > 10
        try:
            fare = float(row['Fare'])
            if fare > 10:
                total_fare += fare
                fare_count += 1

                # Process Trip Miles for maximum (only for this record)
                try:
                    trip_miles = float(row['Trip Miles'])
                    if trip_miles > max_trip_miles:
                        max_trip_miles = trip_miles
                except (ValueError, KeyError):
                    # Skip invalid or missing trip miles
                    pass
        except (ValueError, KeyError):
            # Skip invalid or missing fare values
            pass

# Calculate average fare
if fare_count > 0:
    average_fare = total_fare / fare_count
else:
    average_fare = 0.0

# Print results
print(f"Total of all fares: ${total_fare:.2f}")
print(f"Average fare: ${average_fare:.2f}")
print(f"Maximum trip distance: {max_trip_miles} miles")