# Open the file names.txt and read its contents and print the humnber of names

file_object = open("names.txt")
contents = file_object.read()
print (contents)
file_object.close()