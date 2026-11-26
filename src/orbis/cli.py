"""Command-line interface for ORBIS Core."""

from __future__ import annotations

import argparse
import platform
import shutil
import sys

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="orbis",
        description="ORBIS Linux — The World Intelligence Operating System",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("info", help="show ORBIS Core and host information")
    commands.add_parser("doctor", help="check basic ORBIS development requirements")
    return parser


def run_info() -> int:
    print("ORBIS Linux — The World Intelligence Operating System")
    print(f"ORBIS Core: {__version__}")
    print(f"Host: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print("Image status: not built yet")
    return 0


def run_doctor() -> int:
    checks = {
        "Python 3.10+": sys.version_info >= (3, 10),
        "Git": shutil.which("git") is not None,
    }
    for label, passed in checks.items():
        print(f"[{'OK' if passed else 'MISSING'}] {label}")
    return 0 if all(checks.values()) else 1


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "info":
        return run_info()
    if args.command == "doctor":
        return run_doctor()
    build_parser().print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
