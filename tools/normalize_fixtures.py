#!/usr/bin/env python3
"""Normalize .sip fixtures: collapse blank lines in headers only; keep body."""

from __future__ import annotations

from pathlib import Path

FIX = Path(__file__).resolve().parents[1] / "fixtures"


def normalize(text: str) -> bytes:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    parts = text.split("\n\n", 1)
    header = parts[0]
    body = parts[1] if len(parts) > 1 else ""
    header_lines = [ln for ln in header.split("\n") if ln.strip() != ""]
    out = "\r\n".join(header_lines) + "\r\n\r\n"
    if body:
        # body may already end with newline
        out += body.replace("\n", "\r\n")
        if not out.endswith("\r\n"):
            out += "\r\n"
    return out.encode("utf-8")


def main() -> None:
    for path in sorted(FIX.glob("*.sip")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        path.write_bytes(normalize(raw))
        print(f"normalized {path.name}")


if __name__ == "__main__":
    main()
