"""Tests for body / SDP oracle axes."""

from sipdrift.drivers.builtin import BuiltinDriver
from sipdrift.drivers.sofia_stub import SofiaStubDriver
from sipdrift.harness import COMPARE_AXES, CompareStatus
from sipdrift.parse import (
    body_sha256_raw,
    extract_body_axes,
    normalize_sdp,
    sdp_sha256,
)
from sipdrift.run import run_compare


def test_compare_axes_include_body():
    assert "content_type" in COMPARE_AXES
    assert "body_sha256" in COMPARE_AXES
    assert "sdp_sha256" in COMPARE_AXES


def test_normalize_sdp_strips_trail_ws():
    raw = "v=0  \r\ns=x\r\n\r\n"
    assert normalize_sdp(raw) == "v=0\ns=x\n"


def test_extract_body_axes_invite_sdp():
    ctype, clen, body_h, sdp_h = extract_body_axes(
        "INVITE sip:a@b SIP/2.0\r\n"
        "Content-Type: application/sdp\r\n"
        "Content-Length: 5\r\n\r\n"
        "v=0\n"
    )
    assert ctype == "application/sdp"
    assert clen == 5
    assert body_h == body_sha256_raw("v=0\n")
    assert sdp_h == sdp_sha256("v=0\n", ctype)


def test_extract_compact_ctype():
    ctype, clen, body_h, sdp_h = extract_body_axes(
        "INVITE sip:a@b SIP/2.0\r\n"
        "c: application/sdp\r\n"
        "l: 4\r\n\r\n"
        "v=0\n"
    )
    assert ctype == "application/sdp"
    assert clen == 4
    assert body_h is not None
    assert sdp_h is not None


def test_no_body_axes_when_empty():
    ctype, clen, body_h, sdp_h = extract_body_axes(
        "OPTIONS sip:a@b SIP/2.0\r\nVia: SIP/2.0/UDP h\r\n\r\n"
    )
    assert ctype is None
    assert clen is None
    assert body_h is None
    assert sdp_h is None


def test_sdp_fixture_agree_stubs():
    case = run_compare("F-INVITE-SDP", BuiltinDriver(), SofiaStubDriver())
    assert case.status == CompareStatus.AGREE
    assert case.left.content_type == "application/sdp"
    assert case.left.sdp_sha256 is not None
    assert case.left.body_sha256 is not None


def test_message_body_agree():
    case = run_compare("F-MESSAGE-BODY", BuiltinDriver(), SofiaStubDriver())
    assert case.status == CompareStatus.AGREE
    assert case.left.content_type == "text/plain"
    assert case.left.sdp_sha256 is None
    assert case.left.body_sha256 is not None


def test_sdp_trail_ws_raw_differs_from_norm():
    case = run_compare("F-SDP-TRAIL-WS", BuiltinDriver(), SofiaStubDriver())
    assert case.status == CompareStatus.AGREE
    assert case.left.body_sha256 != case.left.sdp_sha256
