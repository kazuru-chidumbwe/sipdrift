"""Compare run loop: fixture → drivers → classify → report."""

from __future__ import annotations

import json
from typing import Any

from sipdrift.drivers.protocol import StackDriver
from sipdrift.fixtures import load_fixture
from sipdrift.harness import CompareCase, CompareStatus, classify_start_lines


def run_compare(
    fixture_id: str,
    left: StackDriver,
    right: StackDriver,
) -> CompareCase:
    """Load a fixture and compare observations from two stack drivers."""
    raw = load_fixture(fixture_id)
    left_obs = left.observe(raw)
    right_obs = right.observe(raw)
    return classify_start_lines(fixture_id, left_obs, right_obs)


def observation_to_dict(obs: Any) -> dict[str, Any]:
    return {
        "stack_id": obs.stack_id,
        "start_line": obs.start_line,
        "ok": obs.ok,
        "detail": obs.detail,
    }


def case_to_dict(case: CompareCase) -> dict[str, Any]:
    return {
        "fixture_id": case.fixture_id,
        "status": case.status.value,
        "left": observation_to_dict(case.left),
        "right": observation_to_dict(case.right),
        "notes": list(case.notes),
    }


def format_report(case: CompareCase, fmt: str = "text") -> str:
    """Render a CompareCase as text or JSON."""
    if fmt == "json":
        return json.dumps(case_to_dict(case), indent=2, sort_keys=True) + "\n"

    if fmt != "text":
        raise ValueError(f"unknown report format: {fmt!r}")

    lines = [
        f"fixture: {case.fixture_id}",
        f"status:  {case.status.value}",
        f"left:    {case.left.stack_id} ok={case.left.ok} start_line={case.left.start_line!r}",
        f"right:   {case.right.stack_id} ok={case.right.ok} start_line={case.right.start_line!r}",
    ]
    if case.notes:
        lines.append("notes:")
        lines.extend(f"  - {note}" for note in case.notes)
    return "\n".join(lines) + "\n"


def compare_exit_code(status: CompareStatus) -> int:
    """Map compare status to process exit code."""
    if status == CompareStatus.AGREE:
        return 0
    if status in (CompareStatus.DIVERGE, CompareStatus.ERROR):
        return 1
    return 2
