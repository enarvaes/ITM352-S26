# Defining the data [cite: 6, 7]
durations_miles = [1.1, 0.8, 2.5, 2.6]
fares_tuple = ["$6.25", "$5.25", "$10.50", "$8.95"]

# Storing in a dictionary [cite: 8]
taxiTrips = {
    "miles": durations_miles,
    "fares": fares_tuple
}

# Printing results [cite: 9, 12]
print(taxiTrips)

print(f"The third trip was {taxiTrips['miles'][2]} miles long.")
print(f"The fare for the third trip was {taxiTrips['fares'][2]}")