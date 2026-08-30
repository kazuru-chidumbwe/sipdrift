"""CLI entrypoint."""

from __future__ import annotations

import argparse
import sys

from sipdrift import __version__
from sipdrift.drivers.registry import get_driver, list_driver_names
from sipdrift.fixtures import list_fixtures
from sipdrift.run import (
    compare_exit_code,
    format_report,
    format_suite_report,
    run_compare,
    run_suite,
    suite_exit_code,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sipdrift",
        description="SIP/VoIP stack differential testing harness.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"sipdrift {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Show harness version and status.")
    subparsers.add_parser("fixtures", help="List pinned fixture corpus.")

    drivers_parser = subparsers.add_parser("drivers", help="List registered stack drivers.")
    drivers_parser.set_defaults(command="drivers")

    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare a fixture across two stack drivers.",
    )
    compare_parser.add_argument("fixture_id", help="Stable fixture ID (e.g. F-200-MIN).")
    compare_parser.add_argument("--left", default="builtin", help="Left driver name.")
    compare_parser.add_argument("--right", default="pjsip-stub", help="Right driver name.")
    compare_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Report format (default: text).",
    )

    suite_parser = subparsers.add_parser(
        "suite",
        help="Compare all fixtures across two stack drivers.",
    )
    suite_parser.add_argument("--left", default="builtin", help="Left driver name.")
    suite_parser.add_argument("--right", default="pjsip-stub", help="Right driver name.")
    suite_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Report format (default: text).",
    )

    args = parser.parse_args(argv)

    if args.command is None:
        print(f"sipdrift {__version__}: compare harness (early development).")
        return 0

    if args.command == "status":
        print(f"sipdrift {__version__}: compare harness (early development).")
        return 0

    if args.command == "fixtures":
        rows = list_fixtures()
        for fixture_id, path in rows:
            mark = "ok" if path.is_file() else "MISSING"
            print(f"{fixture_id}\t{mark}\t{path.name}")
        return 0 if all(p.is_file() for _, p in rows) else 1

    if args.command == "drivers":
        for name in list_driver_names():
            print(name)
        return 0

    if args.command in ("compare", "suite"):
        try:
            left = get_driver(args.left)
            right = get_driver(args.right)
        except KeyError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

        if args.command == "compare":
            try:
                case = run_compare(args.fixture_id, left, right)
            except (KeyError, FileNotFoundError) as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 2
            sys.stdout.write(format_report(case, fmt=args.format))
            return compare_exit_code(case.status)

        cases = run_suite(left, right)
        sys.stdout.write(format_suite_report(cases, fmt=args.format))
        return suite_exit_code(cases)

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
