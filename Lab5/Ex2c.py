trip_durations = [1.1, 0.8, 2.5, 2.6]
trip_fares = [6.25, 5.25, 10.50, 8.95]

trips = dict(zip(trip_durations, trip_fares))
print(trips)

trip_num = input("What trip do you want? [1-4]: ")
# We have to make it an integer to trip_num will put it into the function
trip_index = int(trip_num) - 1
# print(f"Duration: {trip_durations[trip_index]} miles")
# This ^ autofill can work but we want to use the dictionary we made
print(f"Duration: {list(trips.keys())[trip_index]} miles")
print(f"Fare: ${list(trips.values())[trip_index]:.2f}")
# Ask copilot Given the trip_durations and trip_fares createa. list of dictionaires where each dictionary represents a trip