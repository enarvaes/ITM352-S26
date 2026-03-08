#Quiz game. sixth version.
#Name: Ethan Narvaes
#Date: February 24, 2026
#Make a list with the questions and correct answers.
#Make Questions a dictionary, to include answer options and the correct choice.
#Allow the user to select the correct answer by a label
#Improve look and usability. Keep track of correct answers

import json
import time
import os
import random

# ensure file access works even when running from project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def make_path(filename):
    """Return an absolute path for a filename located next to this script."""
    return os.path.join(BASE_DIR, filename)

"""
Quiz Application
This program allows users to take a multiple-choice quiz from a JSON file.
It tracks high scores, offers hints and 50/50 lifelines, and awards speed bonuses.
"""

def load_json_data(filepath):
    """Safely loads and returns data from a JSON file.

    The provided path may be relative; we resolve it against the script
    directory so that the program works regardless of the current working
    directory (e.g. running from project root versus the A1 folder).
    """
    if not os.path.isabs(filepath):
        filepath = make_path(filepath)
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def calculate_score_with_bonus(time_taken):
    """
    Non-trivial function: Calculates points based on response speed.
    Base points: 10. Bonus: up to 10 extra points if answered under 10 seconds.
    """
    base_points = 10
    # Requirement 9: Bonus points for fastest correct answers
    bonus = max(0, 10 - int(time_taken)) 
    return base_points + bonus

def save_and_check_highscore(name, score):
    """Requirement 1 & 2: Saves score history and notifies user of new high scores."""
    score_data = load_json_data('scores.json')
    history = score_data.get('history', [])
    
    # Identify previous high score
    current_high = max([entry['score'] for entry in history], default=0)
    
    if score > current_high and len(history) > 0:
        print(f"\n✨ NEW HIGH SCORE! You surpassed the previous record of {current_high}! ✨")
    
    # Append new result
    history.append({
        "name": name,
        "score": score,
        "date": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    
    with open(make_path('scores.json'), 'w') as file:
        json.dump({"history": history}, file, indent=4)

def run_quiz():
    # Load questions from external file (Requirement: easy to add/remove)
    data = load_json_data('question.json')
    if not data:
        print("No quiz data found in question.json.")
        return

    # Requirement 5: Choose a category
    print("--- QUIZ CATEGORIES ---")
    categories = list(data.keys())
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    
    selection = input("\nSelect a category number: ")
    # Requirement: Program should not allow invalid responses
    while not selection.isdigit() or int(selection) not in range(1, len(categories) + 1):
        selection = input("Invalid choice. Please enter a valid category number: ")
    
    chosen_cat = categories[int(selection) - 1]
    questions = data[chosen_cat]
    
    total_score = 0
    used_5050 = False # Requirement 10: 50/50 can only be used once per game

    for q in questions:
        print(f"\nQUESTION: {q['question']}")
        opts = q['options']
        correct_ids = q['correct_indices'] # Requirement 4: Multiple correct answers
        
        # Display options (a-d format)
        valid_letters = [chr(97 + i) for i in range(len(opts))]
        for i, opt in enumerate(opts):
            print(f"  {chr(97 + i)}) {opt}")

        start_time = time.time() # Requirement 9: Timer start
        
        while True:
            # Dynamic prompt based on available features
            prompt = f"Answer ({valid_letters[0]}-{valid_letters[-1]}) | 'h' for hint"
            if not used_5050: prompt += " | '5' for 50/50"
            
            user_input = input(f"{prompt}: ").lower().strip()

            if user_input == 'h': # Requirement 6: Provide a hint
                print(f"HINT: {q.get('hint', 'No hint available for this one.')}")
                continue
            
            if user_input == '5' and not used_5050: # Requirement 10: 50/50
                # Identify indices that are NOT correct
                wrongs = [i for i in range(len(opts)) if i not in correct_ids]
                removed = random.sample(wrongs, min(2, len(wrongs)))
                print(f"50/50: Options {', '.join([chr(97+r) for r in removed])} are incorrect!")
                used_5050 = True
                continue

            if user_input in valid_letters:
                break
            print("Invalid input. Please choose a valid letter.")

        # Timing and scoring
        elapsed = time.time() - start_time
        user_idx = ord(user_input) - 97

        if user_idx in correct_ids:
            points_earned = calculate_score_with_bonus(elapsed)
            total_score += points_earned
            print(f"CORRECT! You earned {points_earned} points.")
        else:
            print(f"INCORRECT. The correct answer(s): {[chr(97+i) for i in correct_ids]}")
            
        # Requirement 7: Explanations
        print(f"WHY: {q.get('explanation', 'No explanation provided.')}")

    print(f"\n--- QUIZ OVER ---")
    print(f"Final Score: {total_score}")
    
    player = input("Enter your name for the records: ")
    save_and_check_highscore(player, total_score)

if __name__ == "__main__":
    run_quiz()