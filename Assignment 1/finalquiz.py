#Quiz game.
#Name: Ethan Narvaes
#Date: February 24, 2026
#Make a list with the questions and correct answers.
#Make Questions a dictionary, to include answer options and the correct choice.
#Allow the user to select the correct answer by a label
#Improve look and usability. Keep track of correct answers

import json, time, random, os

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, 'question.json')) as f:
    data = json.load(f)

cats = list(data.keys())
if not cats:
    print('no questions found')
    exit()

questions = data[cats[0]]
score = 0

for q in questions:
    print('\n' + q['question'])
    for i,opt in enumerate(q['options']):
        print(f"{chr(97+i)}) {opt}")
    start = time.time()
    ans = input('answer: ').strip().lower()
    valid = [chr(97+i) for i in range(len(q['options']))]
    while ans not in valid:
        ans = input('invalid, try again: ').strip().lower()
    elapsed = time.time() - start
    idx = ord(ans) - 97
    if idx in q['correct_indices']:
        pts = 10 + max(0, 10 - int(elapsed))
        score += pts
        print('correct, +', pts)
    else:
        print('wrong')
    print('Explanation:', q['explanation'])

print('\nfinal score', score)
name = input('your name? ')
try:
    with open(os.path.join(script_dir, 'scores.json')) as f:
        s = json.load(f)
except:
    s = {'history': []}
s['history'].append({'name': name, 'score': score})
with open(os.path.join(script_dir, 'scores.json'), 'w') as f:
    json.dump(s, f)

