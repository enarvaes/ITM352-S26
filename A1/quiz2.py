#Quiz game. Second Version.
#Name: Ethan Narvaes
#Date: February 24, 2026
#Make a list with the questions, and the correct answers.

questions = [
    ("What is the airspeed of a laden swallow in miles/hr?", "12"),
    ("What is the capital of Texas?", "austin"),
    ("The last supper was painted by which artist?", "Da Vinci")
]

for question, correct_answer in questions:
    answer = input(question + ": ")
    if answer.lower() == correct_answer.lower():
        print("Correct!")
    else:
        print(f"Incorrect. The correct answer is {correct_answer}, not {answer!r}.")