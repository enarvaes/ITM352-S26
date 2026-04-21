import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_dir, "quiz_questions.json")

try:
    with open(json_file_path, 'r') as json_file:
        quiz_questions = json.load(json_file)
    
    print("Loaded quiz questions from JSON:")
    print(json.dumps(quiz_questions, indent=4))
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
except json.JSONDecodeError:
    print("Error: The file is not a valid JSON.")