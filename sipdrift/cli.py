"""Minimal CLI entrypoint (scaffold only)."""

from __future__ import annotations

import argparse
import sys

from sipdrift import __version__
from sipdrift.fixtures import list_fixtures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sipdrift",
        description="SIP/VoIP stack differential testing scaffold (not ready for use).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"sipdrift {__version__}",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=("status", "fixtures"),
        help="Scaffold commands only; compare drivers land in later weekends.",
    )
    args = parser.parse_args(argv)

    if args.command is None or args.command == "status":
        print(f"sipdrift {__version__}: early scaffold — not ready for use.")
        return 0

    if args.command == "fixtures":
        rows = list_fixtures()
        for fixture_id, path in rows:
            mark = "ok" if path.is_file() else "MISSING"
            print(f"{fixture_id}\t{mark}\t{path.name}")
        return 0 if all(p.is_file() for _, p in rows) else 1

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
