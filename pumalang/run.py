from pumalang.globals import create_program_scope
from pumalang.interpreter import Interpreter
from pumalang.lexer import Lexer
from pumalang.parser import Parser
from pumalang.values import Context


def run(fn, text, debug=False, program_scope=None):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    if debug:
        print("\033[32m" + "DEBUG: Lexical Analysis OK！" + "\033[39m")
        print(tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    if debug:
        print("\033[32m" + "DEBUG: Syntax Analysis OK！" + "\033[39m")

    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = program_scope if program_scope is not None else create_program_scope()
    result = interpreter.visit(ast.node, context)

    return result.value, result.error