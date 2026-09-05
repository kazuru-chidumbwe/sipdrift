#!/usr/bin/env python3
"""Generate RFC-4475-inspired torture / adversarial SIP fixtures."""

from __future__ import annotations

from pathlib import Path

FIX = Path(__file__).resolve().parents[1] / "fixtures"

# Long but bounded URI (not multi-megabyte — keep CI fast).
_LONG_USER = "a" * 200

CASES: dict[str, tuple[str, str]] = {
    "F-TORTURE-WS-END": (
        "torture_ws_end.sip",
        "INVITE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-ws-end  \n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-ws-end@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-TORTURE-LWS-COLON": (
        "torture_lws_colon.sip",
        "OPTIONS sip:bob@example.com SIP/2.0\n"
        "Via     :   SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-lws\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-lws@example.com\n"
        "CSeq: 1 OPTIONS\n"
        "Content-Length: 0\n\n",
    ),
    "F-TORTURE-ESCAPED-URI": (
        "torture_escaped_uri.sip",
        "INVITE sip:bob%40example.com@proxy.example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-esc\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob%40example.com@proxy.example.com>\n"
        "Call-ID: sipdrift-esc@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-TORTURE-LONG-URI": (
        "torture_long_uri.sip",
        f"INVITE sip:{_LONG_USER}@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-long\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        f"To: <sip:{_LONG_USER}@example.com>\n"
        "Call-ID: sipdrift-long@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-TORTURE-BAD-CLEN": (
        "torture_bad_clen.sip",
        "MESSAGE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-clen\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-clen@example.com\n"
        "CSeq: 1 MESSAGE\n"
        "Content-Type: text/plain\n"
        "Content-Length: 999\n\n"
        "short\n",
    ),
    "F-TORTURE-DUP-VIA": (
        "torture_dup_cseq_via.sip",
        "INVITE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-d1\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-d1\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-dup@example.com\n"
        "CSeq: 1 INVITE\n"
        "CSeq: 2 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-TORTURE-NONASCII": (
        "torture_nonascii_reason.sip",
        "SIP/2.0 480 Temporarily Unavailable\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-na\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-na@example.com\n"
        "CSeq: 1 INVITE\n"
        "Warning: 399 example.com \"café\"\n"
        "Content-Length: 0\n\n",
    ),
    "F-TORTURE-NULL-IN-BODY": (
        "torture_null_claim.sip",
        "MESSAGE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-null\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-null@example.com\n"
        "CSeq: 1 MESSAGE\n"
        "Content-Type: text/plain\n"
        "Content-Length: 4\n\n"
        "ab\x00c",
    ),
    # Expanded RFC 4475–class edges (inspired; not a verbatim RFC dump).
    "F-TORTURE-UNRECOG-HDR": (
        "torture_unrecog_hdr.sip",
        "OPTIONS sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-unrecog\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-unrecog@example.com\n"
        "CSeq: 1 OPTIONS\n"
        "X-Sipdrift-Odd: yes-please\n"
        "Content-Length: 0\n\n",
    ),
    "F-TORTURE-DISPLAY-NAME": (
        "torture_display_name.sip",
        'INVITE sip:bob@example.com SIP/2.0\n'
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-disp\n"
        "Max-Forwards: 70\n"
        'From: "Alice, the caller" <sip:alice@example.com>;tag=a1\n'
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-disp@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-TORTURE-IPV6-VIA": (
        "torture_ipv6_via.sip",
        "OPTIONS sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP [2001:db8::1]:5060;branch=z9hG4bK-v6\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-v6@example.com\n"
        "CSeq: 1 OPTIONS\n"
        "Content-Length: 0\n\n",
    ),
    "F-TORTURE-NO-MAGIC-COOKIE": (
        "torture_no_magic.sip",
        "INVITE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=no-magic-cookie\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-nomagic@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-TORTURE-EMPTY-SUBJECT": (
        "torture_empty_subject.sip",
        "INVITE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-subj\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-subj@example.com\n"
        "CSeq: 1 INVITE\n"
        "Subject:\n"
        "Content-Length: 0\n\n",
    ),
    "F-TORTURE-MULTI-CLEN": (
        "torture_multi_clen.sip",
        "MESSAGE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-mclen\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-mclen@example.com\n"
        "CSeq: 1 MESSAGE\n"
        "Content-Type: text/plain\n"
        "Content-Length: 5\n"
        "Content-Length: 999\n\n"
        "hello",
    ),
    "F-TORTURE-UNKNOWN-SCHEME": (
        "torture_unknown_scheme.sip",
        "INVITE unusual:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-scheme\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <unusual:bob@example.com>\n"
        "Call-ID: sipdrift-scheme@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-TORTURE-REQ-URI-PARAM": (
        "torture_ruri_param.sip",
        "INVITE sip:bob@example.com;user=phone SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-ruri\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-ruri@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
}


def main() -> None:
    FIX.mkdir(parents=True, exist_ok=True)
    for fid, (name, body) in CASES.items():
        # Most as text; null fixture as bytes
        path = FIX / name
        if "\x00" in body:
            path.write_bytes(body.replace("\n", "\r\n").encode("latin-1"))
        else:
            path.write_bytes(body.replace("\n", "\r\n").encode("utf-8"))
        print(f"wrote {fid} -> {name}")


if __name__ == "__main__":
    main()
