#Quiz game. Fourth version.
#Name: Ethan Narvaes
#Date: February 24, 2026
#Make a list with the questions and correct answers.
#Make Questions a dictionary, to include answer options and the correct choice.
#Allow the user to select the correct answer by a label
#Improve look and usability. Keep track of correct answers


questions = {
    "What is the airspeed of a laden swallow in miles/hr?": ("12", "10", "15", "20"),
    "What is the capital of Texas?": ("Austin", "Houston", "Dallas", "San Antonio"),
    "The last supper was painted by which artist?": ("Da Vinci", "Michealangelo", "Raphael", "Donatello")
}

num_correct = 0
for num, (question, options) in enumerate(questions.items(), start=1):
    print(f"Question {num}:")
    print(question)
    correct_answer = options[0] #The first option is the correct answer.
    sorted_options = sorted(options)
    labeled_alternatives = dict(enumerate(sorted_options, start=1))
    for label, alternative in labeled_alternatives.items():
        print(f" {label}. {alternative}")

        answer_label = input("Choice? ")
        answer = labeled_alternatives[answer_label]
        if answer.lower() == correct_answer.lower():
            print("Correct!")
            num_correct += 1
        else:
            print(f"Incorrect. The correct answer is {correct_answer}, not {answer!r}.")
            
    print(f"You got {num_correct} out of {len(questions)} correct.")

