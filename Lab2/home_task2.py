text = input("Enter a word: ")
count = {"Digit": 0, "letter": 0, "Special Character": 0, "space": 0}
for ch in text:
    if ch.isdigit():
        print(ch, "->Digit")
        count["Digit"] += 1
    elif ch.isalpha():
        print(ch, "->letter")
        count["letter"] += 1
    elif ch.isspace():
        print(ch, "->space")
        count["space"] += 1
    else:
        print(ch, "->Special Character")
        count["Special Character"] += 1

print("Summary:")
for key, value in count.items():
    print(f"{key}: {value}")    
