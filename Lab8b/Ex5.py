# Program to remove any scores from a list that are below 50.
 
scores = [60, 45, 30, 85, 10, 90] 

# Reversed the list to avoid skipping elements when removing items
for score in reversed(scores): 
    if score < 50: 
        scores.remove(score) 
print(scores) 
