# Open the file names.txt, add your own name to the end, and print the entire contents

import os

# Get the directory where this script is located for robust file access
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "names.txt")

# Append your name to the end of the file
with open(file_path, 'a') as file_object:
    file_object.write("Ethan, Narvaez\n")

# Read and print the entire contents of the file
with open(file_path, 'r') as file_object:
    contents = file_object.read()
    print("Entire contents of the file:")
    print(contents)