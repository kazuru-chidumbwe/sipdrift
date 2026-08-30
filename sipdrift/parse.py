"""SIP message parse helpers (start-line + header axes)."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SipStartLine:
    """First line of a SIP request or response."""

    raw: str


_STATUS_RE = re.compile(r"^SIP/2\.0\s+(\d{3})\b", re.IGNORECASE)
_REQUEST_RE = re.compile(r"^([A-Z][A-Z0-9_-]*)\s+\S+\s+SIP/2\.0", re.IGNORECASE)


def split_start_line(message: str) -> SipStartLine:
    """Return the first non-empty line as the SIP start-line.

    Raises:
        ValueError: if the message has no non-empty lines.
    """
    for line in message.replace("\r\n", "\n").split("\n"):
        stripped = line.strip()
        if stripped:
            return SipStartLine(raw=stripped)
    raise ValueError("empty SIP message")


def extract_header(message: str, name: str) -> str | None:
    """Return the value of the first header matching ``name`` (case-insensitive)."""
    target = name.lower()
    for line in message.replace("\r\n", "\n").split("\n"):
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            continue
        header_name, _, value = stripped.partition(":")
        if header_name.strip().lower() == target:
            return value.strip()
    return None


def parse_status_code(start_line: str) -> int | None:
    """Extract numeric status code from a SIP response start-line."""
    match = _STATUS_RE.match(start_line.strip())
    if not match:
        return None
    return int(match.group(1))


def parse_method(start_line: str) -> str | None:
    """Extract method name from a SIP request start-line."""
    match = _REQUEST_RE.match(start_line.strip())
    if not match:
        return None
    return match.group(1).upper()
