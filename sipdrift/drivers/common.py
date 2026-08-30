"""Shared driver helpers."""

from __future__ import annotations

from sipdrift.harness import StackObservation
from sipdrift.parse import extract_header, parse_method, parse_status_code, split_start_line


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
            ok=False,
            detail=str(exc),
        )

    start_line = start.raw
    status_code = parse_status_code(start_line)
    if status_code is None:
        # Requests have no status code; store method in detail for debugging only.
        method = parse_method(start_line)
        if method:
            detail = detail or f"request method={method}"

    return StackObservation(
        stack_id=stack_id,
        start_line=start_line,
        status_code=status_code,
        via=extract_header(raw, "Via"),
        cseq=extract_header(raw, "CSeq"),
        ok=True,
        detail=detail,
    )
