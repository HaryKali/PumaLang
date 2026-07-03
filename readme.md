# ZeroLang

ZeroLang is a small interpreted programming language implemented in Python. It is expression-oriented, dynamically typed, and designed for learning language implementation fundamentals.

Based on: https://github.com/davidcallanan/py-myopl-code

## Highlights

- Simple syntax with familiar operators
- Variables, strings, lists, dictionaries (hash maps), and user-defined functions
- Control flow including `if`, `for`, `while`, `return`, `break`, and `continue`
- Built-in functions for input/output and list manipulation
- Modular interpreter package under `zerolang/`
- Professional CLI with **basic** and **debug** run modes
- Legacy single-file implementation preserved under `onefile/`

## Requirements

- Python 3.10 or higher

## Quick Start

From the project root, start the interactive shell (recommended):

```bash
python -m zerolang.shell
```

Run a script file:

```bash
python -m zerolang.shell examples/hello_world.zero
```

Enable debug mode (lexer/parser diagnostics):

```bash
python -m zerolang.shell -d examples/test_arithmetic.zero
```

You can also invoke the shell directly:

```bash
python zerolang/shell.py examples/hello_world.zero
```

### Shell Run Modes

| Mode | Flag | Behavior |
|------|------|----------|
| **Basic** (default) | *(none)* | Only program output (`print`, etc.) and errors |
| **Debug** | `-d` / `--debug` | Also prints lexer/parser diagnostics |

The shell does **not** echo interpreter return values automatically. Use `print()` when you want output.

### Legacy Single-File Version

The original all-in-one implementation is kept under `onefile/`:

```bash
python onefile/shell.py
python onefile/shell.py examples/hello_world.zero
```

This version always prints lexical/syntax debug messages during execution.

## Using ZeroLang from Python

Recommended (modular package):

```python
from zerolang import run

value, error = run("<stdin>", 'print("Hello World")')
if error:
    print(error.as_string())
```

With debug diagnostics:

```python
from zerolang import run

value, error = run("<stdin>", "1 + 2", debug=True)
```

Legacy single-file import:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path("onefile").resolve()))
import ZeroLang

value, error = ZeroLang.run("<stdin>", 'print("Hello World")')
```

## Program Structure

ZeroLang programs are parsed as sequences of statements. Statements can be separated by semicolons (`;`) or physical newlines. Both are supported.

Example:

```plaintext
var x = 1
var y = 2
print(x + y)
```

Single-line comments begin with `#`.

## Keywords

```
var and or not if then elif else for to step while func end return continue break
```

## Data Types

- Number (integer or float)
- String
- List
- Dict (string or numeric keys)
- Function
- NULL
- Boolean-like values (`TRUE`, `FALSE`, `True`, `False`)

## Operators

### Arithmetic

| Operator | Example | Result |
|----------|---------|--------|
| `+` | `1 + 2` | `3` |
| `-` | `2 - 1` | `1` |
| `*` | `2 * 2` | `4` |
| `/` | `2 / 2` | `1.0` |
| `^` | `2 ^ 2` | `4` |

### Comparison

`==` `!=` `<` `>` `<=` `>=`

### Logical

`and` `or` `not`

## Variables

```plaintext
var x = 10
var name = "ZeroLang"
var arr = [1, 2, 3]
```

## Control Flow

### If Expression

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

### For Loop

```plaintext
for i = 0 to 5 then print(i)
for i = 10 to 0 step -2 then print(i)
```

### While Loop

```plaintext
var i = 0
while i < 3 then var i = i + 1
```

## Functions

Single expression:

```plaintext
func add(a, b) -> a + b
print(add(2, 3))
```

With block and return:

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

List access uses division syntax:

```plaintext
var seq = [10, 20, 30]
print(seq / 1)
```

You can also index lists with square brackets (see [Dictionaries](#dictionaries)).

## Dictionaries

Dictionaries are unordered maps from keys to values. Literal syntax mirrors common brace notation: comma-separated `key: value` pairs inside `{` `}`. Keys and values are arbitrary expressions; at runtime each **key** must evaluate to a **string** or **number**.

```plaintext
var d = {"a": 1, "b": 2}
var k = "a"
print(d[k])
print(d["b"])
```

Empty dictionary:

```plaintext
var empty = {}
```

Use square brackets for lookup: `dict[key]`. The same subscript syntax works for lists, so `seq[1]` is equivalent to `seq / 1` for numeric indices.

```plaintext
var seq = [10, 20, 30]
print(seq[1])
```

## Built-in Functions

Core functions:

- `print(value)`
- `print_ret(value)`
- `input()`
- `input_int()`
- `clear()` / `cls()`

Type checking:

- `is_number(value)`
- `is_string(value)`
- `is_list(value)`
- `is_function(value)`

List operations:

- `append(list, value)`
- `pop(list, index)`
- `extend(listA, listB)`
- `len(list)`
- `sort(target_list, reverse)`

Script execution:

- `run(filename)`

Compatibility aliases (`is_sum`, `is_str`, `is_fun`, `exetend`) are also registered.

## Running Scripts from the REPL

From within the REPL (`python -m zerolang.shell`):

```plaintext
run("examples/test_fibonacci.zero")
```

Launcher scripts are also supported:

```plaintext
# examples/run_fibonacci.zero
run("examples/test_fibonacci.zero")
```

Then run from the shell:

```bash
python -m zerolang.shell examples/run_fibonacci.zero
```

## Examples

The `examples/` directory includes:

- `hello_world.zero`
- `test_arithmetic.zero`
- `test_if.zero`
- `test_loops.zero`
- `test_function.zero`
- `test_lists.zero`
- `test_dict.zero`
- `test_builtins.zero`
- `test_comments_newlines.zero`
- `test_fibonacci.zero`
- `test_fibonacci_iterative.zero`
- `run_fibonacci.zero`
- `run_fibonacci2.zero`

## Error Reporting

ZeroLang provides detailed error reporting for:

- Lexical errors
- Syntax errors
- Runtime errors (with traceback)

Errors include source location information using arrows to point to the offending code.

## Project Structure

```
ZeroLang/
├── zerolang/                  # Main modular interpreter (recommended)
│   ├── __init__.py            # Public package API
│   ├── shell.py               # CLI / REPL entry point
│   ├── run.py                 # Compile-and-run driver
│   ├── lexer.py               # Tokenizer
│   ├── parser.py              # Recursive descent parser
│   ├── interpreter.py         # AST visitor and evaluation
│   ├── nodes.py               # AST node definitions
│   ├── tokens.py              # Token definitions and Position
│   ├── values.py              # Runtime value types
│   ├── builtins.py            # Built-in functions
│   ├── globals.py             # Global symbol table
│   ├── errors.py              # Error classes and formatting
│   ├── strings_with_arrows.py # Source error pointer visualization
│   └── rtresult.py            # Runtime result / control flow
├── onefile/                   # Legacy single-file implementation
│   ├── ZeroLang.py            # All-in-one interpreter
│   ├── strings_with_arrows.py
│   └── shell.py               # CLI for the legacy version
├── examples/                  # Sample .zero programs
├── grammar.txt                # Language grammar notes
├── LICENSE.txt
└── readme.md
```

## Notes

- The modular shell defaults to **basic mode**; use `-d` for lexer/parser debug output
- The legacy `onefile/` interpreter always prints lexical/syntax debug messages
- All variables share a single global symbol table
- The implementation prioritizes educational clarity over performance optimizations
