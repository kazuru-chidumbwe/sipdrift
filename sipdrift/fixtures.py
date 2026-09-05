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
    "F-TORTURE-WS-END": "torture_ws_end.sip",
    "F-TORTURE-LWS-COLON": "torture_lws_colon.sip",
    "F-TORTURE-ESCAPED-URI": "torture_escaped_uri.sip",
    "F-TORTURE-LONG-URI": "torture_long_uri.sip",
    "F-TORTURE-BAD-CLEN": "torture_bad_clen.sip",
    "F-TORTURE-DUP-VIA": "torture_dup_cseq_via.sip",
    "F-TORTURE-NONASCII": "torture_nonascii_reason.sip",
    "F-TORTURE-NULL-IN-BODY": "torture_null_claim.sip",
    "F-TORTURE-UNRECOG-HDR": "torture_unrecog_hdr.sip",
    "F-TORTURE-DISPLAY-NAME": "torture_display_name.sip",
    "F-TORTURE-IPV6-VIA": "torture_ipv6_via.sip",
    "F-TORTURE-NO-MAGIC-COOKIE": "torture_no_magic.sip",
    "F-TORTURE-EMPTY-SUBJECT": "torture_empty_subject.sip",
    "F-TORTURE-MULTI-CLEN": "torture_multi_clen.sip",
    "F-TORTURE-UNKNOWN-SCHEME": "torture_unknown_scheme.sip",
    "F-TORTURE-REQ-URI-PARAM": "torture_ruri_param.sip",
    "F-INVITE-SDP": "invite_sdp.sip",
    "F-200-SDP": "response_200_sdp.sip",
    "F-SDP-TRAIL-WS": "sdp_trail_ws.sip",
    "F-COMPACT-CTYPE": "compact_ctype.sip",
    "F-MESSAGE-BODY": "message_body.sip",
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
    return path.read_bytes().decode("utf-8", errors="replace")
