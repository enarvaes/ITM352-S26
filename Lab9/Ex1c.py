# Open the file names.txt and read its contents and print the humnber of names

file_object = open("C:\\Users\\echan\\OneDrive\\Documents\\Github\\ITM352-S26\\ITM352-S26\\Lab9\\names.txt")
contents = file_object.read()
contents_list = contents.splitlines()
print(contents)
print("Number of names:", len(contents_list))
file_object.close()
