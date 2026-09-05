"""Shared driver helpers."""

from __future__ import annotations

from sipdrift.harness import StackObservation
from sipdrift.parse import (
    extract_body_axes,
    extract_header,
    parse_method,
    parse_status_code,
    split_start_line,
)


def observe_from_parse(stack_id: str, raw: str, detail: str = "") -> StackObservation:
    """Build a StackObservation from parse-path axes (reference/stub tier)."""
    try:
        start = split_start_line(raw)
    except ValueError as exc:
        return StackObservation(
            stack_id=stack_id,
            start_line=None,
            status_code=None,
            via=None,
            cseq=None,
            content_type=None,
            content_length=None,
            body_sha256=None,
            sdp_sha256=None,
            ok=False,
            detail=str(exc),
        )

    start_line = start.raw
    status_code = parse_status_code(start_line)
    if status_code is None:
        method = parse_method(start_line)
        if method:
            detail = detail or f"request method={method}"

    content_type, content_length, body_hash, sdp_hash = extract_body_axes(raw)

    return StackObservation(
        stack_id=stack_id,
        start_line=start_line,
        status_code=status_code,
        via=extract_header(raw, "Via") or extract_header(raw, "v"),
        cseq=extract_header(raw, "CSeq"),
        content_type=content_type,
        content_length=content_length,
        body_sha256=body_hash,
        sdp_sha256=sdp_hash,
        ok=True,
        detail=detail,
    )
