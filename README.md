# Compiler Construction Lab

This repository contains Python practical work for the Compiler Construction course.
The exercises introduce file handling, modules, packages, lexical analysis, tokenization,
and basic character classification.

## Repository Structure

```text
.
├── lab1/
│   ├── README.md
│   ├── file_handling.py
│   ├── file.txt
│   ├── import_module.py
│   ├── import_package.py
│   ├── module.py
│   └── packages/
└── Lab2/
    ├── README.md
    ├── home_task2.py
    ├── task1.py
    └── task3.py
```

Lab 3 documentation is available in [`Lab3/README.md`](Lab3/README.md).

## Requirements

- Python 3.10 or newer
- A terminal or Python-compatible IDE
- PLY for Lab 3

Install the Lab 3 dependency with:

```powershell
pip install ply
```

## Running the Labs

Run commands from the repository root:

```powershell
python lab1/file_handling.py
python lab1/import_module.py
python lab1/import_package.py
python Lab2/task1.py
python Lab2/home_task2.py
python Lab2/task3.py
python Lab3/task1.py
```

For module and package examples, running from the repository root is recommended so
Python can resolve the files inside `lab1` correctly. Alternatively, change into the
relevant lab directory before running its scripts.

## Learning Outcomes

- Read, write, count, tokenize, and delete text files with Python.
- Organize reusable functions in modules and packages.
- Classify input characters and simple tokens.
- Scan an arithmetic expression character by character.
- Extract number tokens from a basic expression.
- Build a PLY lexer for keywords, identifiers, numbers, operators, and symbols.

## Notes

- `file_handling.py` deletes `file.txt` at the end of its execution if the file exists.
- The calculator scripts accept two integer values and provide sum, difference,
  multiplication, and division operations.
- Lab 3 requires the third-party PLY package.
- Generated Python cache files are excluded through `.gitignore`.
