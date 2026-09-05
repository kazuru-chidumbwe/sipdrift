"""SIP message parse helpers (start-line, headers, body/SDP)."""

from __future__ import annotations

import hashlib
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


def split_headers_body(message: str) -> tuple[str, str]:
    """Split SIP message into header block and body (after first blank line)."""
    text = message.replace("\r\n", "\n").replace("\r", "\n")
    if "\n\n" in text:
        headers, _, body = text.partition("\n\n")
        return headers, body
    return text, ""


def normalize_sdp(body: str) -> str:
    """Normalize SDP for stable hashing: LF lines, rstrip, drop trailing blanks."""
    lines = [ln.rstrip() for ln in body.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + ("\n" if lines else "")


def body_sha256_raw(body: str) -> str:
    """SHA-256 hex of body as UTF-8 (replacement for bad bytes)."""
    return hashlib.sha256(body.encode("utf-8", errors="replace")).hexdigest()


def sdp_sha256(body: str, content_type: str | None) -> str | None:
    """SHA-256 of normalized SDP, or None when Content-Type is not application/sdp."""
    ctype = (content_type or "").split(";", 1)[0].strip().lower()
    if ctype != "application/sdp":
        return None
    return hashlib.sha256(normalize_sdp(body).encode("utf-8")).hexdigest()


def extract_body_axes(message: str) -> tuple[str | None, int | None, str | None, str | None]:
    """Return (content_type, content_length, body_sha256, sdp_sha256)."""
    headers, body = split_headers_body(message)
    header_blob = headers + "\n\n"
    ctype = extract_header(header_blob, "Content-Type")
    if ctype is None:
        ctype = extract_header(header_blob, "c")
    clen_raw = extract_header(header_blob, "Content-Length")
    if clen_raw is None:
        clen_raw = extract_header(header_blob, "l")
    try:
        clen = int(clen_raw) if clen_raw is not None else None
    except ValueError:
        clen = None
    if not body and clen is None and ctype is None:
        return None, None, None, None
    return ctype, clen, body_sha256_raw(body), sdp_sha256(body, ctype)
