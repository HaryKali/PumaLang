from pumalang.builtins import BuiltInFunction
from pumalang.values import Number, SymbolTable

# Names registered on the global (builtin) symbol table.
BUILTIN_NAMES = frozenset({
    "NULL", "False", "True", "FALSE", "TRUE", "MATH_PI",
    "print", "print_ret", "input", "input_int", "clear", "cls",
    "is_number", "is_string", "is_function", "is_list",
    "is_sum", "is_str", "is_fun",
    "append", "pop", "extend", "exetend", "sort", "len", "run",
})


def _register_builtins(table: SymbolTable):
    table.set("NULL", Number.null)
    table.set("False", Number.false)
    table.set("True", Number.true)
    table.set("FALSE", Number.false)
    table.set("TRUE", Number.true)
    table.set("MATH_PI", Number.math_PI)
    table.set("print", BuiltInFunction.print)
    table.set("print_ret", BuiltInFunction.print_ret)
    table.set("input", BuiltInFunction.input)
    table.set("input_int", BuiltInFunction.input_int)
    table.set("clear", BuiltInFunction.clear)
    table.set("cls", BuiltInFunction.clear)
    table.set("is_number", BuiltInFunction.is_number)
    table.set("is_string", BuiltInFunction.is_string)
    table.set("is_function", BuiltInFunction.is_function)
    table.set("is_sum", BuiltInFunction.is_number)
    table.set("is_str", BuiltInFunction.is_string)
    table.set("is_list", BuiltInFunction.is_list)
    table.set("is_fun", BuiltInFunction.is_function)
    table.set("append", BuiltInFunction.append)
    table.set("pop", BuiltInFunction.pop)
    table.set("extend", BuiltInFunction.extend)
    table.set("exetend", BuiltInFunction.extend)
    table.set("sort", BuiltInFunction.sort)
    table.set("len", BuiltInFunction.len)
    table.set("run", BuiltInFunction.run)


def create_global_symbol_table() -> SymbolTable:
    """Create the root global symbol table containing builtins and constants."""
    table = SymbolTable(parent=None, is_global=True)
    _register_builtins(table)
    return table


def create_program_scope(parent=None) -> SymbolTable:
    """
    Create a fresh program scope layered on top of the global symbol table.

    User-defined globals (`var` at top level) live here and do not overwrite
  builtins in the root global table.
    """
    root = parent if parent is not None else global_symbol_table
    return SymbolTable(parent=root)


global_symbol_table = create_global_symbol_table()
