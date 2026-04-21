import json
import os

quiz_questions = {
    "General": [
        {
            "question": "What is the capital of France?",
            "options": ["Lyon", "Marseille", "Paris", "Nice"],
            "correct_indices": [2],
            "hint": "It's known as the City of Light.",
            "explanation": "Paris has been the capital of France since the 10th century."
        },
        {
            "question": "Which element has the chemical symbol 'O'?",
            "options": ["Gold", "Oxygen", "Silver", "Iron"],
            "correct_indices": [1],
            "hint": "It's essential for respiration.",
            "explanation": "Oxygen's symbol comes from its name."
        },
        {
            "question": "In which continent is Brazil located?",
            "options": ["Asia", "Africa", "South America", "Europe"],
            "correct_indices": [2],
            "hint": "Think of the Amazon rainforest.",
            "explanation": "Brazil is the largest country in South America."
        },
        {
            "question": "What is 7 × 8?",
            "options": ["54", "56", "64", "49"],
            "correct_indices": [1],
            "hint": "It's one more than 55.",
            "explanation": "7 multiplied by 8 equals 56."
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Venus", "Mars", "Jupiter", "Saturn"],
            "correct_indices": [1],
            "hint": "It's the fourth planet from the sun.",
            "explanation": "Mars appears red due to iron oxide on its surface."
        }
    ]
}

questions_only = [q["question"] for q in quiz_questions["General"]]

script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_dir, "quiz_questions.json")

with open(json_file_path, 'w') as json_file:
    json.dump(questions_only, json_file, indent=4)

print(f"List of quiz questions saved to {json_file_path}")