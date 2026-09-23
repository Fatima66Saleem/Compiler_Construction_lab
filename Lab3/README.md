# Lab 3: PLY Lexer

Lab 3 implements a lexical analyzer using the Python Lex-Yacc (PLY) library.
The lexer reads a line of source code and prints the tokens it recognizes.

## Files

### `task1.py`

Defines a PLY lexer that recognizes:

- Reserved keywords: `if`, `else`, `while`, `for`, `int`, and `return`
- Identifiers, including letters, digits, and underscores
- Integer and decimal number literals
- Arithmetic operators: `+`, `-`, `*`, and `/`
- Assignment and comparison operators: `=`, `>=`, `<=`, `==`, `!=`, `>`, and `<`
- Parentheses, brackets, braces, commas, and semicolons
- Python-style comments beginning with `#`

Spaces and tabs are ignored. Integer tokens are converted to `int` values and
decimal tokens are converted to `float` values.

Run the lexer from the repository root:

```powershell
python Lab3/task1.py
```

Example input:

```text
int total = 12.5 + value >= 10;
```

### `ply_lexer_notes.md`

Contains explanatory notes on lexer concepts, token rules, reserved keywords,
regular expressions, and the PLY workflow.

## Requirement

Install PLY before running the lexer:

```powershell
pip install ply
```

## Concepts Practiced

- Building a lexer with `ply.lex`
- Defining token rules with regular expressions
- Recognizing identifiers and reserved keywords
- Converting numeric token values
- Ignoring whitespace and comments
- Scanning source code one token at a time