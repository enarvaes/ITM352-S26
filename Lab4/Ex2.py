# Define a list of survey reponse values (5, 7, 3, 8) and store them in a
# variable. Next define a tuple of respondent ID values (1012, 1035, 1021, and 1053).
# Use the .append() method to append the tuple to the list. Print out the list.

#responses = [5, 7, 3, 8]
#respondent_ids = (1012, 1035, 1021, 1053)
#responses.append(respondent_ids)
#print("Survey Responses with Respondent IDs:", responses)

response_values = [(1012, 5), (1035, 7), (1021, 3), (1053, 8)]
response_values.sort()
print("Sorted Survey Responses with Respondent IDs:", response_values)
