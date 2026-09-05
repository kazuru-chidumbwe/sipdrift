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
    "F-100-TRYING": "response_100_trying.sip",
    "F-180-RINGING": "response_180_ringing.sip",
    "F-401-AUTH": "response_401_auth.sip",
    "F-404-NOTFOUND": "response_404_notfound.sip",
    "F-603-DECLINE": "response_603_decline.sip",
    "F-ACK-MIN": "ack_min.sip",
    "F-BYE-MIN": "bye_min.sip",
    "F-CANCEL-MIN": "cancel_min.sip",
    "F-INFO-MIN": "info_min.sip",
    "F-MESSAGE-MIN": "message_min.sip",
    "F-NOTIFY-MIN": "notify_min.sip",
    "F-SUBSCRIBE-MIN": "subscribe_min.sip",
    "F-COMPACT-VIA": "compact_via.sip",
    "F-MULTI-VIA": "multi_via.sip",
    "F-FOLDED-VIA": "folded_via.sip",
    "F-LOWER-SIP": "lower_sip_version.sip",
    "F-SPACES-START": "spaces_start.sip",
    "F-TAB-SEP": "tab_sep_headers.sip",
    "F-UNKNOWN-METHOD": "unknown_method.sip",
    "F-NO-HEADERS": "no_headers.sip",
    "F-ONLY-START": "only_start_line.sip",
    "F-JUNK-AFTER": "junk_after_message.sip",
    "F-MISSING-VIA": "missing_via.sip",
    "F-MISSING-CSEQ": "missing_cseq.sip",
    "F-BAD-STATUS": "bad_status_code.sip",
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
