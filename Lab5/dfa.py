def dfa(s):
    state = 'q0'
    for ch in s:
        if state == 'q0':
            if ch == "a":
                state = "q0"
            elif ch == "b":
                state = "q1"
            else:
                return ("Rejected")
        elif state == "q1":
            if ch == "b":
                state = "q1"
            elif ch == "a":
                state = "q0"
            else:
                return ("Rejected")

    if state == "q0":
        return "Accepted"
    else:
        return "Rejected"

print(dfa("abba"))