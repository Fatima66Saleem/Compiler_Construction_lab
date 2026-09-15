# Lab 1

Lab 1 covers Python file handling and code organization with modules and packages.
These exercises provide a foundation for separating reusable functionality before
moving to compiler-oriented processing.

## Files

### `file_handling.py`

Demonstrates:

- Creating and writing to `file.txt`
- Reading lines and complete file content
- Counting lines and words
- Splitting content into simple tokens
- Classifying tokens as numbers, identifiers, punctuation, or unknown values
- Deleting `file.txt` after processing

Run it with:

```powershell
python file_handling.py
```

Because the script writes and deletes `file.txt`, run it in the `lab1` directory.

### `module.py` and `import_module.py`

`module.py` contains arithmetic functions for sum, difference, multiplication, and
division. `import_module.py` imports that module and provides an interactive menu.

Run from the `lab1` directory:

```powershell
python import_module.py
```

### `packages/` and `import_package.py`

The `packages` directory contains separate arithmetic modules:

- `sum.py`
- `diff.py`
- `mul.py`
- `div.py`

`import_package.py` imports these functions individually and exposes the same
interactive calculator menu.

Run from the `lab1` directory:

```powershell
python import_package.py
```

## Concepts Practiced

- File input and output
- Basic lexical tokenization
- Python modules
- Python packages
- Function reuse and imports
- Interactive command-line programs
