import pandas as pd

# List of individuals' ages
ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]

# Lists of individuals' names and genders
names = ["Joe", "Jaden", "Max", "Sidney", "Evgeni", "Taylor", "Pia", "Luis", "Blanca", "Cyndi"]
gender = ["M", "M", "M", "F", "M", "F", "F", "M", "F", "F"]

# Create a list of (age, gender) tuples
tuple_list = list(zip(ages, gender))
print("List of (age, gender) tuples:")
print(tuple_list)

# Create a dataframe from the list of tuples
df = pd.DataFrame(tuple_list, index=names, columns=["Age", "Gender"])
print("\nDataFrame:")
print(df)

# Summary statistics
summary = df.describe()
print("\nSummary statistics:")
print(summary)

# Average age by gender
average_age_by_gender = df.groupby("Gender")["Age"].mean()
print("\nAverage age by gender:")
print(average_age_by_gender)

