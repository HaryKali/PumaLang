#!/usr/bin/env python3
"""
ZeroLang 单文件版命令行入口（onefile/ZeroLang.py）

用法:
    python onefile/shell.py                  # 交互式 REPL
    python onefile/shell.py script.zero      # 运行脚本
"""

import argparse
import sys
from pathlib import Path

ONEFILE_DIR = Path(__file__).resolve().parent
if str(ONEFILE_DIR) not in sys.path:
    sys.path.insert(0, str(ONEFILE_DIR))

import ZeroLang


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"


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

VERSION = "0.1.0 (onefile)"
EXIT_COMMANDS = {"exit", "quit", "bye"}


def format_value(value):
    if value is None:
        return None
    if hasattr(value, "elements"):
        if len(value.elements) == 1:
            return repr(value.elements[0])
        return repr(value.elements)
    return repr(value)


def print_banner():
    print(f"{Colors.CYAN}{Colors.BOLD}{BANNER}{Colors.RESET}")
    print(f"{Colors.GREEN}ZeroLang Shell v{VERSION}{Colors.RESET}")
    print("输入 exit / quit / bye 或按 Ctrl+C 退出")
    print("=" * 60)


def execute_source(filename, source, *, echo_filename=False):
    if echo_filename:
        print(f"{Colors.GREEN}Running: {filename}{Colors.RESET}")

    result, error = ZeroLang.run(filename, source)
    if error:
        print(f"{Colors.RED}{error.as_string()}{Colors.RESET}")
        return False

    formatted = format_value(result)
    if formatted is not None:
        print(f"{Colors.CYAN}{formatted}{Colors.RESET}")
    return True


def run_repl():
    print_banner()

    while True:
        try:
            text = input(f"{Colors.GREEN}{Colors.BOLD}ZeroLang (onefile) > {Colors.RESET}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.YELLOW}再见！{Colors.RESET}")
            break

        if not text.strip():
            continue
        if text.strip().lower() in EXIT_COMMANDS:
            print(f"{Colors.YELLOW}会话已结束。{Colors.RESET}")
            break

        execute_source("<stdin>", text)


def run_file(filepath: Path):
    if not filepath.is_file():
        print(f"{Colors.RED}错误：找不到文件 {filepath}{Colors.RESET}")
        sys.exit(1)

    if filepath.suffix != ".zero":
        print(f"{Colors.YELLOW}警告：文件扩展名不是 .zero{Colors.RESET}")

    try:
        source = filepath.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"{Colors.RED}读取文件失败：{exc}{Colors.RESET}")
        sys.exit(1)

    if not execute_source(str(filepath.resolve()), source, echo_filename=True):
        sys.exit(1)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="zerolang-onefile",
        description="ZeroLang 单文件版解释器命令行入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python onefile/shell.py\n"
            "  python onefile/shell.py ../examples/hello_world.zero"
        ),
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        help="要执行的 .zero 源文件（省略则进入 REPL）",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"ZeroLang {VERSION}",
    )

    args = parser.parse_args(argv)

    if args.file:
        run_file(args.file)
    else:
        run_repl()


if __name__ == "__main__":
    main()
