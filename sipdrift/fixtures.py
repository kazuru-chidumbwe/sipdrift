"""Fixture loading helpers (scaffold)."""

from __future__ import annotations

from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"

# Stable IDs for JOSS-era manifests later.
FIXTURE_INDEX: dict[str, str] = {
    "F-INVITE-MIN": "invite_min.sip",
    "F-200-MIN": "response_200_min.sip",
    "F-486-MIN": "response_486_busy.sip",
    "F-503-MIN": "response_503_unavail.sip",
    "F-OPTIONS-MIN": "options_min.sip",
    "F-REGISTER-MIN": "register_min.sip",
    "F-MALFORMED-START": "malformed_start.sip",
}


def list_fixtures() -> list[tuple[str, Path]]:
    """Return (fixture_id, path) pairs in index order."""
    rows: list[tuple[str, Path]] = []
    for fixture_id, name in FIXTURE_INDEX.items():
        path = FIXTURES_DIR / name
        rows.append((fixture_id, path))
    return rows


def load_fixture(fixture_id: str) -> str:
    """Load a fixture by stable ID.

    Raises:
        KeyError: unknown fixture id.
        FileNotFoundError: file missing on disk.
    """
    try:
        name = FIXTURE_INDEX[fixture_id]
    except KeyError as exc:
        raise KeyError(f"unknown fixture id: {fixture_id}") from exc
    path = FIXTURES_DIR / name
    return path.read_text(encoding="utf-8")
