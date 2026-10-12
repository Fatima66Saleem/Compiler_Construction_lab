def dfa(s):
    state = 'q0'
    for ch in s:
        if state == 'q0':
            if ch == "a":
                state = "q0"
                state = "q1"
            elif ch == "b":
                state = "q0"
            else:
                return ("Rejected")

    if state == "q1":
        return "Accepted"
    else:
        return "Rejected"

print(dfa("abba"))