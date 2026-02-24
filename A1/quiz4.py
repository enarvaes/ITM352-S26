#Quiz game. Fourth version.
#Name: Ethan Narvaes
#Date: February 24, 2026
#Make a list with the questions and correct answers.
#Make Questions a dictionary, to include answer options and the correct choice.
#Allow the user to select the correct answer by a label

questions = {
    "What is the airspeed of a laden swallow in miles/hr?": ("12", "10", "15", "20"),
    "What is the capital of Texas?": ("Austin", "Houston", "Dallas", "San Antonio"),
    "The last supper was painted by which artist?": ("Da Vinci", "Michealangelo", "Raphael", "Donatello")
}

for question, options in questions.items():
    correct_answer = options[0] #The first option is the correct answer.
    sorted_options = sorted(options)
    for label, alternative in enumerate(sorted_options, start=1): 
        print(f" {label}. {alternative}")
    answer = input(question + ": ")
    answer = sorted_options[int(answer) - 1]
    if answer.lower() == correct_answer.lower():
        print("Correct!")
    else:
        print(f"Incorrect. The correct answer is {correct_answer}, not {answer!r}.")