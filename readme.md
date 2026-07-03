# PumaLang

PumaLang is a small interpreted programming language implemented in Python. It is expression-oriented, dynamically typed, and designed for learning language implementation fundamentals.

Based on: [py-myopl-code](https://github.com/davidcallanan/py-myopl-code)

## Highlights

- Simple syntax with familiar operators
- Variables, strings, lists, dictionaries, and user-defined functions
- Control flow: `if`, `for`, `while`, `return`, `break`, `continue`
- Built-in I/O and list manipulation functions
- Modular interpreter package under `pumalang/`
- CLI shell with **basic** / **debug** modes
- Legacy single-file implementation under `onefile/`

## Requirements

- Python 3.10+

## Quick Start

Start the interactive shell from the project root:

```bash
python -m pumalang.shell
```

Run a `.pumalang` script:

```bash
python -m pumalang.shell examples/hello_world.pumalang
```

Run with lexer/parser diagnostics:

```bash
python -m pumalang.shell -d examples/test_arithmetic.pumalang
```

Alternative entry point:

```bash
python pumalang/shell.py examples/hello_world.pumalang
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `python -m pumalang.shell` | Open REPL (basic mode) |
| `python -m pumalang.shell <file>` | Execute a `.pumalang` file |
| `python -m pumalang.shell -d <file>` | Execute with debug diagnostics |
| `python -m pumalang.shell -v` | Print version and exit |

### Run Modes

| Mode | Flag | Output |
|------|------|--------|
| **Basic** (default) | — | Program `print` output and errors only |
| **Debug** | `-d` / `--debug` | Also shows lexer/parser diagnostics |

The shell does **not** echo interpreter return values. Use `print()` for visible output.

### Legacy Single-File Shell

```bash
python onefile/shell.py
python onefile/shell.py examples/hello_world.pumalang
```

The `onefile/` interpreter always prints lexical/syntax debug messages.

## Using PumaLang from Python

Modular package (recommended):

```python
from pumalang import run

value, error = run("<stdin>", 'print("Hello World")')
if error:
    print(error.as_string())
```

With debug diagnostics:

```python
from pumalang import run

value, error = run("<stdin>", "1 + 2", debug=True)
```

Legacy single-file import:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path("onefile").resolve()))
import pumalang

value, error = pumalang.run("<stdin>", 'print("Hello World")')
```

## Language Overview

PumaLang source files use the **`.pumalang`** extension. Programs are sequences of statements separated by `;` or newlines.

```plaintext
var x = 1
var y = 2
print(x + y)
```

Comments start with `#`.

### Keywords

```
var and or not if then elif else for to step while func end return continue break
```

### Data Types

| Type | Notes |
|------|-------|
| Number | Integer or float |
| String | Double-quoted literals |
| List | `[1, 2, 3]` |
| Dict | `{"key": value}` — keys must be strings or numbers |
| Function | User-defined or built-in |
| NULL | `NULL` |
| Boolean | `TRUE`, `FALSE`, `True`, `False` |

### Operators

**Arithmetic:** `+` `-` `*` `/` `^`

**Comparison:** `==` `!=` `<` `>` `<=` `>=`

**Logical:** `and` `or` `not`

## Control Flow

### If

Expression form:

```plaintext
if x > 0 then 1 elif x == 0 then 0 else -1
```

Block form:

```plaintext
if x > 0 then
    print("positive")
else
    print("not positive")
end
```

### For

```plaintext
for i = 0 to 5 then print(i)
for i = 10 to 0 step -2 then print(i)
```

### While

```plaintext
var i = 0
while i < 3 then var i = i + 1
```

## Functions

Arrow (single-expression) form:

```plaintext
func add(a, b) -> a + b
print(add(2, 3))
```

Block form with `return`:

```plaintext
func sum_to(n)
    var total = 0
    for i = 1 to n + 1 then var total = total + i
    return total
end
print(sum_to(5))
```

## Lists

```plaintext
var l = [3, 1, 2]
append(l, 5)
print(l)
print(pop(l, 1))
sort(l, 0)
print(l)
print(len(l))
```

Index with `/` or `[]`:

```plaintext
var seq = [10, 20, 30]
print(seq / 1)
print(seq[1])
```

## Dictionaries

```plaintext
var d = {"a": 1, "b": 2}
print(d["a"])
print(d["b"])
```

Empty dict: `var empty = {}`

## Built-in Functions

| Category | Functions |
|----------|-----------|
| I/O | `print`, `print_ret`, `input`, `input_int`, `clear` / `cls` |
| Type checks | `is_number`, `is_string`, `is_list`, `is_function` |
| Lists | `append`, `pop`, `extend`, `len`, `sort` |
| Scripts | `run(filename)` |

Aliases: `is_sum`, `is_str`, `is_fun`, `exetend`.

## Running Scripts

From the REPL:

```plaintext
run("examples/test_fibonacci.pumalang")
```

Or use a launcher script:

```bash
python -m pumalang.shell examples/run_fibonacci.pumalang
```

## Examples

| File | Topic |
|------|-------|
| `hello_world.pumalang` | Hello World |
| `test_arithmetic.pumalang` | Arithmetic |
| `test_if.pumalang` | Conditionals |
| `test_loops.pumalang` | Loops |
| `test_function.pumalang` | Functions |
| `test_lists.pumalang` | Lists |
| `test_dict.pumalang` | Dictionaries |
| `test_builtins.pumalang` | Built-ins |
| `test_comments_newlines.pumalang` | Comments & newlines |
| `test_fibonacci.pumalang` | Recursive Fibonacci |
| `test_fibonacci_iterative.pumalang` | Iterative Fibonacci |
| `run_fibonacci.pumalang` | Script launcher |

## Error Reporting

PumaLang reports lexical, syntax, and runtime errors with source locations and caret arrows pointing at the offending code. Runtime errors include a traceback through function call contexts.

## Project Structure

```
PumaLang/
├── pumalang/                  # Modular interpreter (recommended)
│   ├── __init__.py            # Public package API
│   ├── shell.py               # CLI / REPL entry point
│   ├── run.py                 # Compile-and-run driver
│   ├── lexer.py               # Tokenizer
│   ├── parser.py              # Recursive descent parser
│   ├── interpreter.py         # AST visitor / evaluator
│   ├── nodes.py               # AST node definitions
│   ├── tokens.py              # Tokens and Position
│   ├── values.py              # Runtime value types
│   ├── builtins.py            # Built-in functions
│   ├── globals.py             # Global symbol table
│   ├── errors.py              # Error classes
│   ├── strings_with_arrows.py # Error pointer rendering
│   └── rtresult.py            # Control-flow result wrapper
├── onefile/                   # Legacy single-file interpreter
│   ├── pumalang.py
│   ├── strings_with_arrows.py
│   └── shell.py
├── examples/                  # Sample .pumalang programs
├── grammar.txt
├── LICENSE.txt
└── readme.md
```

## Notes

- Source files use the `.pumalang` extension
- Modular shell defaults to **basic mode**; pass `-d` for debug output
- Return values are not printed automatically — use `print()`
- All variables currently share a single global symbol table
- Implementation prioritizes educational clarity over performance
