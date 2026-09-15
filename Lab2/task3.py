text = "x + y"
pos = 0
while pos < len(text):
    current_char = text[pos]
    print(f"Position: {pos}: '{current_char}'")
    pos += 1


# --------task 3: Tokenize numbers in an arithmetic expression---------

text = "123 + 456"
pos = 0
token = []


while pos < len(text):
    ch = text[pos]
    if ch.isdigit():
        num = ""
        while pos < len(text) and text[pos].isdigit():
            num += text[pos]
            pos += 1
        token.append(("Number", num))
    else:
        pos += 1

print(token)

