"""Compare-harness: observations, axes, and classification."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CompareStatus(str, Enum):
    """Outcome of one fixture across two stack observations."""

    AGREE = "agree"
    DIVERGE = "diverge"
    ERROR = "error"
    SKIP = "skip"  # driver missing / not implemented


# Oracle axes compared in Phase 2 (start-line + selected headers).
COMPARE_AXES: tuple[str, ...] = ("start_line", "status_code", "via", "cseq")


@dataclass(frozen=True)
class StackObservation:
    """What one SIP stack produced for a fixture."""

    stack_id: str
    start_line: str | None
    ok: bool
    status_code: int | None = None
    via: str | None = None
    cseq: str | None = None
    detail: str = ""


@dataclass
class CompareCase:
    """One fixture evaluated under two observations."""

    fixture_id: str
    left: StackObservation
    right: StackObservation
    status: CompareStatus = CompareStatus.SKIP
    notes: list[str] = field(default_factory=list)


def _axis_value(obs: StackObservation, axis: str) -> object:
    return getattr(obs, axis)


def classify_observations(
    fixture_id: str,
    left: StackObservation,
    right: StackObservation,
    axes: tuple[str, ...] = COMPARE_AXES,
) -> CompareCase:
    """Compare observations on named axes when both sides succeeded."""
    case = CompareCase(fixture_id=fixture_id, left=left, right=right)

    if not left.ok or not right.ok:
        case.status = CompareStatus.ERROR
        case.notes.append("one or both observations failed")
        return case

    if left.start_line is None or right.start_line is None:
        case.status = CompareStatus.SKIP
        case.notes.append("start-line not available (driver stub)")
        return case

    mismatches: list[str] = []
    for axis in axes:
        left_val = _axis_value(left, axis)
        right_val = _axis_value(right, axis)
        if left_val != right_val:
            mismatches.append(
                f"{axis} mismatch: {left.stack_id!r}={left_val!r} vs "
                f"{right.stack_id!r}={right_val!r}"
            )

    if mismatches:
        case.status = CompareStatus.DIVERGE
        case.notes.extend(mismatches)
    else:
        case.status = CompareStatus.AGREE
    return case


def classify_start_lines(
    fixture_id: str,
    left: StackObservation,
    right: StackObservation,
) -> CompareCase:
    """Backward-compatible alias — full axis compare."""
    return classify_observations(fixture_id, left, right)
