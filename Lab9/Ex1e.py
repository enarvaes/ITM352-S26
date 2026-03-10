# Open the file names.txt and read its contents and print the humnber of names

from importlib.resources import contents


file_object = open("names.txt")
contents_lists = file_object.readlines()
print(contents_lists)
print("Number of names:", len(contents_list))
file_object.close()
