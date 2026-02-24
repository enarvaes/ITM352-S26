#Quiz game. First Version.
#Name: Ethan Narvaes
#Date: Feburary 24, 2026

answer = input("What is the airspeed of a laden swallow in miles/hr?")
if answer == "12":
    print("Correct!")
else:
    print(f"Incorrect. The correct answer is 12 miles/hr, not {answer!r}.")
    
answer = input("What is the captial of Texas?")
if answer.lower() == "austin":
    print("Correct!")
else:
    print(f"Incorrect. The correct answer is Austin, not {answer!r}.")

