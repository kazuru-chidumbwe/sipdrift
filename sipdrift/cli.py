"""Minimal CLI entrypoint (scaffold only)."""

from __future__ import annotations

import argparse
import sys

from sipdrift import __version__


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
        choices=("status",),
        help="Scaffold commands only; more will land in later weekends.",
    )
    args = parser.parse_args(argv)

    if args.command == "status" or args.command is None:
        print(f"sipdrift {__version__}: early scaffold — not ready for use.")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
