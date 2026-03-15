# Open the file names.txt and read its contents and print the humnber of names

with open("C:\\Users\\echan\\OneDrive\\Documents\\Github\\ITM352-S26\\ITM352-S26\\Lab9\\names.txt") as file_object:
    while (line := file_object.readline()) != "":
        print(line.strip())
        