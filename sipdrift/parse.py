"""SIP message parse stubs.

Weekend-2 scope: hold a clear API surface only. No production parser yet.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SipStartLine:
    """First line of a SIP request or response (placeholder)."""

    raw: str


def split_start_line(message: str) -> SipStartLine:
    """Return the first non-empty line as a start-line stub.

    Raises:
        ValueError: if the message has no non-empty lines.
    """
    for line in message.replace("\r\n", "\n").split("\n"):
        stripped = line.strip()
        if stripped:
            return SipStartLine(raw=stripped)
    raise ValueError("empty SIP message")
