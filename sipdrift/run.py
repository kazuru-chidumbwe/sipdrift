"""Compare run loop: fixture → drivers → classify → report."""

from __future__ import annotations

import json
from typing import Any

from sipdrift.drivers.protocol import StackDriver
from sipdrift.fixtures import FIXTURE_INDEX, load_fixture
from sipdrift.harness import CompareCase, CompareStatus, classify_observations


def _short_hash(value: str | None) -> str:
    if value is None:
        return "None"
    return value[:12] + "…" if len(value) > 12 else value


def run_compare(
    fixture_id: str,
    left: StackDriver,
    right: StackDriver,
) -> CompareCase:
    """Load a fixture and compare observations from two stack drivers."""
    raw = load_fixture(fixture_id)
    left_obs = left.observe(raw)
    right_obs = right.observe(raw)
    return classify_observations(fixture_id, left_obs, right_obs)


def run_suite(
    left: StackDriver,
    right: StackDriver,
    fixture_ids: list[str] | None = None,
) -> list[CompareCase]:
    """Compare many fixtures; default is the full pinned corpus."""
    ids = fixture_ids if fixture_ids is not None else list(FIXTURE_INDEX)
    return [run_compare(fixture_id, left, right) for fixture_id in ids]


def observation_to_dict(obs: Any) -> dict[str, Any]:
    return {
        "stack_id": obs.stack_id,
        "start_line": obs.start_line,
        "status_code": obs.status_code,
        "via": obs.via,
        "cseq": obs.cseq,
        "content_type": obs.content_type,
        "content_length": obs.content_length,
        "body_sha256": obs.body_sha256,
        "sdp_sha256": obs.sdp_sha256,
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


def suite_to_dict(cases: list[CompareCase]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for case in cases:
        counts[case.status.value] = counts.get(case.status.value, 0) + 1
    return {
        "summary": counts,
        "cases": [case_to_dict(case) for case in cases],
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
        (
            f"left:    {case.left.stack_id} ok={case.left.ok} "
            f"start_line={case.left.start_line!r} status={case.left.status_code} "
            f"via={case.left.via!r} cseq={case.left.cseq!r} "
            f"ctype={case.left.content_type!r} clen={case.left.content_length} "
            f"body={_short_hash(case.left.body_sha256)} "
            f"sdp={_short_hash(case.left.sdp_sha256)}"
        ),
        (
            f"right:   {case.right.stack_id} ok={case.right.ok} "
            f"start_line={case.right.start_line!r} status={case.right.status_code} "
            f"via={case.right.via!r} cseq={case.right.cseq!r} "
            f"ctype={case.right.content_type!r} clen={case.right.content_length} "
            f"body={_short_hash(case.right.body_sha256)} "
            f"sdp={_short_hash(case.right.sdp_sha256)}"
        ),
    ]
    if case.notes:
        lines.append("notes:")
        lines.extend(f"  - {note}" for note in case.notes)
    return "\n".join(lines) + "\n"


def format_suite_report(cases: list[CompareCase], fmt: str = "text") -> str:
    """Render a suite run as text or JSON."""
    if fmt == "json":
        return json.dumps(suite_to_dict(cases), indent=2, sort_keys=True) + "\n"

    if fmt != "text":
        raise ValueError(f"unknown report format: {fmt!r}")

    summary = suite_to_dict(cases)["summary"]
    parts = [
        "suite summary:",
        *(f"  {key}: {value}" for key, value in sorted(summary.items())),
        "",
    ]
    for case in cases:
        parts.append(format_report(case, fmt="text").rstrip())
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def suite_exit_code(cases: list[CompareCase]) -> int:
    """Exit 0 only when every case agrees."""
    if not cases:
        return 2
    if any(case.status == CompareStatus.SKIP for case in cases):
        return 2
    if any(case.status in (CompareStatus.DIVERGE, CompareStatus.ERROR) for case in cases):
        return 1
    return 0


def compare_exit_code(status: CompareStatus) -> int:
    """Map compare status to process exit code."""
    if status == CompareStatus.AGREE:
        return 0
    if status in (CompareStatus.DIVERGE, CompareStatus.ERROR):
        return 1
    return 2
