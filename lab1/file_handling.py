
# WRITE OPERATION

f = open("file.txt", "w") # open text file for writing
f.write(" My name is Fatima \n I am learning file handling in Python \n a + b = result_ab") # write content to the file
f.close() # close the file after writing


# READ OPERATION

f = open("file.txt", "r") #  open text file
lines = f.readlines() # read all lines into a list
print("Lines:", lines)
f.close() # close the file after reading all lines
 
f = open("file.txt", "r") # open text file for reading entire content
content = f.read() # read the entire content of the file
print("Content:\n", content) # display the entire content of the file

# COUNT METHOD -> Number of Lines & Number of Words
num_lines = len(content.splitlines()) # count the number of lines in the content
num_words = len(content.split()) # count the number of words in the content

print("Number of Lines:", num_lines)
print("Number of Words:", num_words)

f.close()





# TOKENIZATION -> Lexical Analysis with Token Classes
tokens = content.split()  # tokenization => lexical analysis
print("\nTokens:", tokens)

print("\n--- TOKEN CLASSES ---")
for t in tokens:
    if t.isdigit(): # isdigit -> checks if the token is a number
        print(t, "-> number")
    elif t.isidentifier(): # isidentifier -> checks if the token is a valid identifier
        print(t, "-> identifier")
    elif t in [".", ",", "!", "?", ";", ":"]: # checks if the token is a punctuation mark
        print(t, "-> punctuation")
    else:
        print(t, "-> unknown")


# DELETE OPERATION -> Removing file.txt from system
import os # os checks the files in system

if os.path.exists("file.txt"): # check if the file exists before attempting to delete it
    os.remove("file.txt") # delete the file from the system
    print("\nfile.txt successfully deleted from system.")
else:
    print("\nfile.txt does not exist.") # inform the user that the file was not found