import string

#Read file
with open("paragraph.txt", "r") as file:
    text = file.read()

#Split text into sentences
import re
sentences = re.split(r'[.!?]',text)
sentences = [sentence.strip() for sentence in sentences if sentence.strip()] #Remove empty strings

#Create list of words
words = text.translate(str.maketrans('', '', string.punctuation)).split()#Remove punctuation and split
#Create set of words
unique_words = set(words)

#Find the hidden message
indices = [60, 26, 10, 10, 41, 35, 26, 44, 48]
hidden_message = ''.join([words[i][0] for i in indices])

#Print results and answers
print(len(sentences)) #10
print(len(unique_words)) #81
print(hidden_message) #hApptCAts
