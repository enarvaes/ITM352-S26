# Open the file names.txt and read its contents and print the number of names

import os

# Get the directory where this script is located for robust file access
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "names.txt")

file_object = open(file_path)
contents_lists = file_object.readlines()
print(contents_lists)
print("Number of names:", len(contents_lists))

# Example: Put the names in a dictionary (assuming each line is "key, value")
names_dict = {}
for line in contents_lists:
    parts = line.strip().split(', ')
    if len(parts) == 2:
        names_dict[parts[0]] = parts[1]

print("Names dictionary:", names_dict)
file_object.close()