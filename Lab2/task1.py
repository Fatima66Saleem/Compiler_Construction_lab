
# split the given code into words and classify each token
code = "int a = 5.0 ;"
tokens = code.split() # split the code into words based on spaces
for ch in tokens:
    if ch.isdigit():
        print(ch, "->Digit")
    elif ch.isalpha():
        print(ch, "->letter")
    else:
        print(ch, "->Special Character")
print(tokens)

# character by character
code = "int a=5.0;"
i = 0
while i < len(code):
    print(code[i])
    i += 1

# ignore spaces
code = "int a=5.0;"
i = 0
while i < len(code):
    if code[i].isspace():
        i = i+1
        continue
    print(code[i])
    i += 1






