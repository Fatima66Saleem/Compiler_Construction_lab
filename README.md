# Compiler Construction Lab

A comprehensive Python practical course covering foundational compiler concepts: file handling, modules, packages, lexical analysis, tokenization, and finite automata.

**Language:** Python 3.10+  
**Topics:** File I/O • Modules & Packages • Tokenization • Lexical Analysis • NFA/DFA

---

## 📁 Repository Structure

```
Compiler_Construction_lab/
├── README.md
├── lab1/
│   ├── README.md
│   ├── file_handling.py
│   ├── file.txt
│   ├── import_module.py
│   ├── import_package.py
│   ├── module.py
│   └── packages/
├── Lab2/
│   ├── README.md
│   ├── task1.py
│   ├── home_task2.py
│   └── task3.py
├── Lab3/
│   ├── README.md
│   ├── task.py
│   ├── task.txt
│   └── ply_lexer_notes.md
├── Lab4/
│   ├── README.md
│   └── nfa.py
├── Lab5/
│   ├── README.md
│   ├── dfa.py
│   └── nfa.py
└── .gitignore
```

---

## 📚 Lab Overview

### Lab 1: File Handling, Modules & Packages
- Read/write text files
- Import modules and build reusable code
- Understand package structure

### Lab 2: Lexical Analysis & Tokenization
- Inspect characters and classify tokens
- Handle whitespace and token boundaries
- Extract numeric tokens from expressions

### Lab 3: PLY Lexer
- Build a lexer with Python `ply`
- Recognize keywords, numbers, operators, and identifiers
- Handle comments and invalid characters

### Lab 4: NFA Concepts
- Understand finite automata states and transitions
- Learn how abstract machines accept or reject inputs

### Lab 5: DFA Concepts
- Build deterministic state machines
- Practice final-state acceptance checks
- Connect automata ideas to compiler theory

---

## 🚀 Run the Labs

```bash
# Lab 1
python lab1/file_handling.py
python lab1/import_module.py
python lab1/import_package.py

# Lab 2
python Lab2/task1.py
python Lab2/home_task2.py
python Lab2/task3.py

# Lab 3
pip install ply
python Lab3/task.py

# Lab 4
python Lab4/nfa.py

# Lab 5
python Lab5/dfa.py
```

---

## 📖 Learning Outcomes

- File handling and Python program structure
- Module/package organization
- Lexical scanning and token extraction
- PLY lexer construction
- Finite automata and compiler-design basics

---

## Notes

- Lab 4 and Lab 5 introduce compiler theory foundations used in lexical analysis and parsing.
- Lab 3 requires the `ply` package.
- Some scripts should be run from the repository root so relative imports work correctly.
