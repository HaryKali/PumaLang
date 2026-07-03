#!/usr/bin/env python3
"""
ZeroLang command-line shell for the modular interpreter.

Usage:
    python -m zerolang.shell                  # REPL (basic mode)
    python -m zerolang.shell script.zero      # run a script (basic mode)
    python -m zerolang.shell -d script.zero   # run with debug diagnostics
"""

import argparse
import sys
from enum import Enum
from pathlib import Path


def _ensure_package_path():
    # Allow `python zerolang/shell.py` to resolve the zerolang package.
    if __package__:
        return
    root = Path(__file__).resolve().parent.parent
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


_ensure_package_path()

from zerolang.run import run


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    DIM = "\033[2m"


class RunMode(Enum):
    """Shell output mode."""

    BASIC = "basic"   # default: program output and errors only
    DEBUG = "debug"   # additionally show lexer/parser diagnostics


BANNER = r"""
 ________                       __
/\_____  \                     /\ \
\/____//'/'     __   _ __   ___\ \ \         __      ___      __
     //'/'    /'__`\/\`'__\/ __`\ \ \  __  /'__`\  /' _ `\  /'_ `\
    //'/'___ /\  __/\ \ \//\ \L\ \ \ \L\ \/\ \L\.\_/\ \/\ \/\ \L\ \
    /\_______\ \____\\ \_\\ \____/\ \____/\ \__/.\_\ \_\ \_\ \____ \
    \/_______/\/____/ \/_/ \/___/  \/___/  \/__/\/_/\/_/\/_/\/___L\ \
                                                              /\____/
                                                              \_/__/
"""

VERSION = "0.2.0"
EXIT_COMMANDS = {"exit", "quit", "bye"}


def print_banner(mode: RunMode):
    print(f"{Colors.CYAN}{Colors.BOLD}{BANNER}{Colors.RESET}")
    mode_label = mode.value.upper()
    print(f"{Colors.GREEN}ZeroLang Shell v{VERSION} [{mode_label}]{Colors.RESET}")
    print("Type exit, quit, bye, or press Ctrl+C to leave")
    print("=" * 60)


def execute_source(
    filename,
    source,
    *,
    mode: RunMode = RunMode.BASIC,
    echo_filename: bool = False,
):
    """
    Compile and run source code.

    Basic mode : only runtime output from the program itself, plus errors.
    Debug mode : also prints lexer/parser diagnostics (no return-value echo).
    """
    debug = mode is RunMode.DEBUG

    if echo_filename and debug:
        print(f"{Colors.DIM}Running: {filename}{Colors.RESET}")

    _result, error = run(filename, source, debug=debug)
    if error:
        print(f"{Colors.RED}{error.as_string()}{Colors.RESET}")
        return False

    return True


def run_repl(*, mode: RunMode = RunMode.BASIC):
    print_banner(mode)

    while True:
        try:
            text = input(f"{Colors.GREEN}{Colors.BOLD}ZeroLang > {Colors.RESET}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.YELLOW}Goodbye.{Colors.RESET}")
            break

        if not text.strip():
            continue
        if text.strip().lower() in EXIT_COMMANDS:
            print(f"{Colors.YELLOW}Session ended.{Colors.RESET}")
            break

        execute_source("<stdin>", text, mode=mode)


def run_file(filepath: Path, *, mode: RunMode = RunMode.BASIC):
    if not filepath.is_file():
        print(f"{Colors.RED}Error: file not found: {filepath}{Colors.RESET}")
        sys.exit(1)

    if filepath.suffix != ".zero":
        print(f"{Colors.YELLOW}Warning: file does not use the .zero extension.{Colors.RESET}")

    try:
        source = filepath.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"{Colors.RED}Failed to read file: {exc}{Colors.RESET}")
        sys.exit(1)

    # File runs in basic mode stay quiet unless the program prints something.
    if not execute_source(
        str(filepath.resolve()),
        source,
        mode=mode,
        echo_filename=True,
    ):
        sys.exit(1)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="zerolang",
        description="ZeroLang modular interpreter shell",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python -m zerolang.shell\n"
            "  python -m zerolang.shell examples/hello_world.zero\n"
            "  python -m zerolang.shell -d examples/test_arithmetic.zero"
        ),
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        help="Optional .zero source file; opens REPL when omitted",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug mode (lexer/parser diagnostics only)",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"ZeroLang {VERSION}",
    )
    return parser


def resolve_mode(debug_flag: bool) -> RunMode:
    return RunMode.DEBUG if debug_flag else RunMode.BASIC


def main(argv=None):
    args = build_parser().parse_args(argv)
    mode = resolve_mode(args.debug)

    if args.file:
        run_file(args.file, mode=mode)
    else:
        run_repl(mode=mode)


if __name__ == "__main__":
    main()
