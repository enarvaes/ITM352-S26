#An example of creating and using your own function
#Name: Ethan Narvaes
#Date: 1/22/2026
import datetime

def greet(name):
    """This function greets the person whose name is paseed in. In addition we want to print a welcome message that include the day of the week."""
    message = "Hello" + " " + name + "!"
    x = datetime.datetime.now()
    day_of_week = x.strftime("%A")
    message += " Happy" + " " + day_of_week + "."
    return message

user_name = input("Enter your name: ")
greeting_message = greet(user_name)
print(greeting_message)
