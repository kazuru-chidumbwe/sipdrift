"""Tests for parse helpers."""

from sipdrift.parse import extract_header, parse_method, parse_status_code, split_start_line


def test_parse_status_code_200():
    assert parse_status_code("SIP/2.0 200 OK") == 200


def test_parse_status_code_none_for_request():
    assert parse_status_code("INVITE sip:bob@example.com SIP/2.0") is None


def test_parse_method_invite():
    assert parse_method("INVITE sip:bob@example.com SIP/2.0") == "INVITE"


def test_extract_header_via():
    msg = "SIP/2.0 200 OK\r\nVia: SIP/2.0/UDP host;branch=z9hG4bK\r\n\r\n"
    assert extract_header(msg, "via") == "SIP/2.0/UDP host;branch=z9hG4bK"


def test_extract_header_cseq():
    msg = "INVITE sip:a@b SIP/2.0\r\nCSeq: 42 INVITE\r\n\r\n"
    assert extract_header(msg, "CSeq") == "42 INVITE"
