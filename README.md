# Compiler Construction Lab

A comprehensive Python practical course covering foundational compiler concepts: file handling, modules, packages, lexical analysis, tokenization, and building a complete lexer using PLY (Python Lex-Yacc).

**Language:** Python 3.10+  
**Topics:** File I/O • Modules & Packages • Character Classification • Tokenization • Lexical Analysis

---

## 📁 Repository Structure

```
Compiler_Construction_lab/
├── README.md
├── lab1/                     # File Handling, Modules & Packages
│   ├── README.md
│   ├── file_handling.py
│   ├── file.txt
│   ├── import_module.py
│   ├── import_package.py
│   ├── module.py
│   └── packages/
├── Lab2/                     # Basic Lexical Analysis & Tokenization
│   ├── README.md
│   ├── task1.py
│   ├── home_task2.py
│   └── task3.py
└── Lab3/                     # PLY Lexer Implementation
    ├── README.md
    ├── task.py
    ├── task.txt
    └── ply_lexer_notes.md
```

---

## 📚 Labs Overview

### **Lab 1: File Handling, Modules & Packages**

**Objective:** Learn Python fundamentals including file operations and code organization.

| File | Purpose |
|------|---------|
| `file_handling.py` | Demonstrates reading, writing, counting, and deleting text files |
| `file.txt` | Sample text file for file operations |
| `module.py` | Reusable module with arithmetic functions (sum, diff, mul, div) |
| `import_module.py` | Interactive calculator that imports and uses functions from `module.py` |
| `import_package.py` | Example of importing from Python packages |
| `packages/` | Directory structure demonstrating package organization |

**Key Concepts:**
- Reading and writing text files with Python
- Creating and importing modules
- Package structure and organization
- Code reusability through imports

**Run Lab 1:**
```bash
python lab1/file_handling.py
python lab1/import_module.py
python lab1/import_package.py
```

---

### **Lab 2: Basic Lexical Analysis & Tokenization**

**Objective:** Introduce scanner fundamentals: character examination, token classification, and basic expression parsing.

| File | Purpose |
|------|---------|
| `task1.py` | Token classification and character-by-character scanning of `int a = 5.0 ;` |
| `home_task2.py` | User input: classify characters and generate summary statistics |
| `task3.py` | Extract number tokens from arithmetic expression `123 + 456` |

**Concepts Practiced:**
- Character-by-character scanning
- Whitespace handling and skipping
- Character classification (digits, letters, special characters, spaces)
- Token boundary recognition
- Integer literal extraction
- Building token lists with (token_type, value) pairs

**Run Lab 2:**
```bash
# Task 1: Tokenize sample code
python Lab2/task1.py

# Task 2: User input with character classification
python Lab2/home_task2.py

# Task 3: Extract number tokens from expression
python Lab2/task3.py
```

**Example Output (task2):**
```
Enter a word: int123
i ->letter
n ->letter
t ->letter
1 ->Digit
2 ->Digit
3 ->Digit
Summary:
Digit: 3
letter: 3
Special Character: 0
space: 0
```

---

### **Lab 3: PLY Lexer Implementation**

**Objective:** Build a production-grade lexical analyzer using the PLY (Python Lex-Yacc) library.

| File | Purpose |
|------|---------|
| `task.py` | Complete lexer recognizing keywords, identifiers, operators, numbers, and symbols |
| `ply_lexer_notes.md` | Comprehensive guide to PLY concepts, regex patterns, and lexer workflow |
| `task.txt` | Future tasks for GUI implementation |

**Lexer Features:**
- **Keywords:** `if`, `else`, `while`, `for`, `int`, `return`
- **Identifiers:** Variables like `x`, `value_1`, `_temp`
- **Numbers:** Integer (`123`) and decimal (`45.67`) literals
- **Operators:** Arithmetic (`+`, `-`, `*`, `/`) and Comparison (`==`, `!=`, `>=`, `<=`, `>`, `<`)
- **Delimiters:** Parentheses, brackets, braces, commas, semicolons
- **Comments:** Python-style (`#` to end of line)
- **Whitespace:** Automatically ignored

**Concepts Practiced:**
- Regular expression patterns for token matching
- Reserved word detection with dictionaries
- Token value conversion (string → int/float)
- Comment handling
- Error reporting with line numbers
- PLY lexer workflow and token generation

**Run Lab 3:**
```bash
# First, install PLY
pip install ply

# Run the lexer
python Lab3/task.py
```

**Example:**
```
Enter code: int total = 12.5 + value >= 10;
LexToken(INT,'int',1,0)
LexToken(ID,'total',1,4)
LexToken(EQUALS,'=',1,10)
LexToken(Number,12.5,1,12)
LexToken(PLUS,'+',1,17)
LexToken(ID,'value',1,19)
LexToken(GE,'>=',1,25)
LexToken(Number,10,1,28)
LexToken(SEMICOLON,';',1,30)
```

---

## ⚙️ Requirements & Setup

### System Requirements
- **Python:** 3.10 or newer
- **Terminal/IDE:** Any Python-compatible environment

### Installation

**Clone the repository:**
```bash
git clone https://github.com/Fatima66Saleem/Compiler_Construction_lab.git
cd Compiler_Construction_lab
```

**Install Lab 3 dependency (PLY):**
```bash
pip install ply
```

---

## 🚀 Running All Labs

Run commands from the repository root for proper module resolution:

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
python Lab3/task.py
```

---

## 📖 Learning Path

This course follows a **progressive** curriculum:

1. **Lab 1** → Foundation: File I/O and Python organization
2. **Lab 2** → Scanner basics: Understanding character and token analysis
3. **Lab 3** → Complete lexer: Production implementation with PLY

Each lab builds on previous knowledge, moving from simple character classification to a full-featured lexical analyzer.

---

## 🎓 Learning Outcomes

After completing these labs, you will understand:

✅ How to perform file I/O operations in Python  
✅ How to organize code using modules and packages  
✅ How character-by-character scanning works  
✅ How to classify and tokenize source code  
✅ How to build and use regular expressions for token matching  
✅ How the lexical analysis phase of a compiler works  
✅ How to use PLY for lexer generation  
✅ How to handle reserved keywords vs. identifiers  
✅ How to report lexical errors with line numbers  

---

## ⚠️ Important Notes

- **Lab 1:** `file_handling.py` deletes `file.txt` upon completion (this is intentional)
- **Lab 2:** Simple examples prepare for more complex lexers; intentionally step-by-step
- **Lab 3:** Requires `pip install ply` before running
- **Module Import:** Run Lab 1 scripts from the repository root so Python can resolve module paths
- **Cache Files:** Generated Python cache (`__pycache__/`, `*.pyc`) are excluded via `.gitignore`

---

## 📝 Additional Resources

- **PLY Documentation:** [PLY Official Docs](http://www.dabeaz.com/ply/)
- **Python Regex Guide:** [Python `re` Module](https://docs.python.org/3/library/re.html)
- **Compiler Design:** See individual lab `README.md` files for detailed concept explanations

---

## 👤 Author

**Fatima66Saleem**

---

## 📄 License

This project is open source and available under the MIT License.
