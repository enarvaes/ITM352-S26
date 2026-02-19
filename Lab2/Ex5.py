#Ask the user to eneter their weight in pounds
#convert the weight to kilograms (1 pound = 0.453592 kg)
#Name: Ethan Narvaes
#Date: 1/22/2026

kg_to_pounds = 0.453592

weight_in_pounds = input("Enter weight in pounds: ")
weight_in_pounds_float = float(weight_in_pounds)
weight_in_kg = weight_in_pounds_float * kg_to_pounds

weight_in_kg = round(weight_in_kg, 2)

print(f"You entered {weight_in_pounds} pounds, which is {weight_in_kg:.2f} kilograms.")