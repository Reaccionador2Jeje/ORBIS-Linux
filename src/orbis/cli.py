"""Command-line interface for ORBIS Core."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys

from . import __version__
from .geojson import GeoJSONError, inspect_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="orbis",
        description="ORBIS Linux — The World Intelligence Operating System",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("info", help="show ORBIS Core and host information")
    commands.add_parser("doctor", help="check basic ORBIS development requirements")

    geojson = commands.add_parser("geojson", help="inspect and validate a GeoJSON file")
    geojson.add_argument("file", help="path to a .geojson or .json file")
    geojson.add_argument("--pretty", action="store_true", help="pretty-print the JSON report")
    return parser


def run_info() -> int:
    print("ORBIS Linux — The World Intelligence Operating System")
    print(f"ORBIS Core: {__version__}")
    print(f"Host: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print("Geospatial engine: GeoJSON inspection enabled")
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


def run_geojson(filename: str, pretty: bool = False) -> int:
    try:
        report = inspect_file(filename)
    except GeoJSONError as exc:
        print(f"ORBIS GeoJSON: INVALID: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2 if pretty else None, sort_keys=True))
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "info":
        return run_info()
    if args.command == "doctor":
        return run_doctor()
    if args.command == "geojson":
        return run_geojson(args.file, args.pretty)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
