"""Compare-harness outline (scaffold — no stack drivers yet).

Weekend-2 intent: lock the *shape* of a differential run so later weekends
only fill drivers + oracles, not redesign the loop.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CompareStatus(str, Enum):
    """Outcome of one fixture across two stack observations."""

    AGREE = "agree"
    DIVERGE = "diverge"
    ERROR = "error"
    SKIP = "skip"  # driver missing / not implemented


@dataclass(frozen=True)
class StackObservation:
    """What one SIP stack produced for a fixture (placeholder fields)."""

    stack_id: str
    start_line: str | None
    ok: bool
    detail: str = ""


@dataclass
class CompareCase:
    """One fixture evaluated under two observations."""

    fixture_id: str
    left: StackObservation
    right: StackObservation
    status: CompareStatus = CompareStatus.SKIP
    notes: list[str] = field(default_factory=list)


def classify_start_lines(
    fixture_id: str,
    left: StackObservation,
    right: StackObservation,
) -> CompareCase:
    """Scaffold classifier: compare start-lines only when both sides ok."""
    case = CompareCase(fixture_id=fixture_id, left=left, right=right)

    if not left.ok or not right.ok:
        case.status = CompareStatus.ERROR
        case.notes.append("one or both observations failed")
        return case

    if left.start_line is None or right.start_line is None:
        case.status = CompareStatus.SKIP
        case.notes.append("start-line not available (driver stub)")
        return case

    if left.start_line == right.start_line:
        case.status = CompareStatus.AGREE
    else:
        case.status = CompareStatus.DIVERGE
        case.notes.append(
            f"start-line mismatch: {left.stack_id!r} vs {right.stack_id!r}"
        )
    return case
