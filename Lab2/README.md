# Lab 2

Lab 2 introduces basic lexical analysis by examining characters and simple tokens.
The programs demonstrate how a scanner can inspect input, skip whitespace, classify
characters, and recognize numbers in an arithmetic expression.

## Files

### `task1.py`

Uses the sample code `int a = 5.0 ;` to demonstrate:

- Splitting source text into simple tokens
- Classifying tokens as digits, letters, or special characters
- Printing source text character by character
- Ignoring whitespace while scanning

Run it with:

```powershell
python task1.py
```

### `home_task2.py`

Reads a word or line from the user and classifies every character as:

- Digit
- Letter
- Space
- Special character

It also prints a count summary for each category.

Run it with:

```powershell
python home_task2.py
```

### `task3.py`

Scans the expression `123 + 456` character by character and extracts consecutive
digit sequences as number tokens. The result is stored as `("Number", value)` pairs.

Run it with:

```powershell
python task3.py
```

## Concepts Practiced

- Character-by-character scanning
- Whitespace handling
- Character classification with Python string methods
- Token boundaries
- Recognizing integer literals
- Building a basic token list

These examples are intentionally simple and prepare the structure needed for a
more complete lexical analyzer.
