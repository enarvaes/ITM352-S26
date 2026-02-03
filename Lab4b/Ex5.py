sentence = input

#Turn a string into a list of words
sentence = input("Enter a sentence: ")
words_list = sentence.split(" ")
print(f"List of words: {words_list}")

#Reverse the list
reversed_list = words_list[::-1]
q=uote_reversed = " ".join(reversed_list)

#print reverse list as a string
new_sentence = " ".join(reversed_list)
print(f"Reversed sentence: {new_sentence}")