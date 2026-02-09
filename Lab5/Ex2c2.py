trip_durations = [1.1, 0.8, 2.5, 2.6]
trip_fares = ["$6.25", "$5.25", "$10.50", "$8.95"]

trips = dict(zip(trip_durations, trip_fares))
print(trips)


trips_list = [
    {"duration": 1.1, "fare": 6.25},
    {"duration": 0.8, "fare": 5.25},
    {"duration": 2.5, "fare": 10.50},
    {"duration": 2.6, "fare": 8.95}
]
print("List of trip dictionaries:")
print(trips_list)


trip_num = input("What trip do you want? [1-4]: ")
trip_index = int(trip_num) - 1


print(f"\nduration: {trips_list[trip_index]['duration']} miles")
print(f"Fare: ${trips_list[trip_index]['fare']:.2f}")