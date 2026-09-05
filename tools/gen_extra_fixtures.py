"""Generate expanded adversarial SIP fixtures for lab experiments."""

from __future__ import annotations

from pathlib import Path

FIX = Path(__file__).resolve().parents[1] / "fixtures"

CASES: dict[str, tuple[str, str]] = {
    # id -> (filename, body)  — bodies use \n; writers normalize to CRLF
    "F-100-TRYING": (
        "response_100_trying.sip",
        "SIP/2.0 100 Trying\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-100\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-100@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-180-RINGING": (
        "response_180_ringing.sip",
        "SIP/2.0 180 Ringing\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-180\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-180@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-401-AUTH": (
        "response_401_auth.sip",
        "SIP/2.0 401 Unauthorized\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-401\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-401@example.com\n"
        "CSeq: 1 REGISTER\n"
        'WWW-Authenticate: Digest realm="example.com", nonce="abc"\n'
        "Content-Length: 0\n\n",
    ),
    "F-404-NOTFOUND": (
        "response_404_notfound.sip",
        "SIP/2.0 404 Not Found\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-404\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-404@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-603-DECLINE": (
        "response_603_decline.sip",
        "SIP/2.0 603 Decline\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-603\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-603@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-ACK-MIN": (
        "ack_min.sip",
        "ACK sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-ack\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-ack@example.com\n"
        "CSeq: 1 ACK\n"
        "Content-Length: 0\n\n",
    ),
    "F-BYE-MIN": (
        "bye_min.sip",
        "BYE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-bye\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-bye@example.com\n"
        "CSeq: 2 BYE\n"
        "Content-Length: 0\n\n",
    ),
    "F-CANCEL-MIN": (
        "cancel_min.sip",
        "CANCEL sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-cancel\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-cancel@example.com\n"
        "CSeq: 1 CANCEL\n"
        "Content-Length: 0\n\n",
    ),
    "F-INFO-MIN": (
        "info_min.sip",
        "INFO sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-info\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-info@example.com\n"
        "CSeq: 3 INFO\n"
        "Content-Length: 0\n\n",
    ),
    "F-MESSAGE-MIN": (
        "message_min.sip",
        "MESSAGE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-msg\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-msg@example.com\n"
        "CSeq: 1 MESSAGE\n"
        "Content-Type: text/plain\n"
        "Content-Length: 5\n\n"
        "hello",
    ),
    "F-NOTIFY-MIN": (
        "notify_min.sip",
        "NOTIFY sip:alice@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.2:5060;branch=z9hG4bK-notify\n"
        "Max-Forwards: 70\n"
        "From: <sip:bob@example.com>;tag=b1\n"
        "To: <sip:alice@example.com>;tag=a1\n"
        "Call-ID: sipdrift-notify@example.com\n"
        "CSeq: 1 NOTIFY\n"
        "Event: presence\n"
        "Subscription-State: active\n"
        "Content-Length: 0\n\n",
    ),
    "F-SUBSCRIBE-MIN": (
        "subscribe_min.sip",
        "SUBSCRIBE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-sub\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-sub@example.com\n"
        "CSeq: 1 SUBSCRIBE\n"
        "Event: presence\n"
        "Expires: 3600\n"
        "Content-Length: 0\n\n",
    ),
    "F-COMPACT-VIA": (
        "compact_via.sip",
        "INVITE sip:bob@example.com SIP/2.0\n"
        "v: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-compact\n"
        "Max-Forwards: 70\n"
        "f: <sip:alice@example.com>;tag=a1\n"
        "t: <sip:bob@example.com>\n"
        "i: sipdrift-compact@example.com\n"
        "CSeq: 1 INVITE\n"
        "m: <sip:alice@192.0.2.1:5060>\n"
        "l: 0\n\n",
    ),
    "F-MULTI-VIA": (
        "multi_via.sip",
        "SIP/2.0 200 OK\n"
        "Via: SIP/2.0/UDP proxy.example.com:5060;branch=z9hG4bK-p1\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-u1\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-multivia@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-FOLDED-VIA": (
        "folded_via.sip",
        "INVITE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;\n"
        " branch=z9hG4bK-folded\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-folded@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-LOWER-SIP": (
        "lower_sip_version.sip",
        "invite sip:bob@example.com sip/2.0\n"
        "via: sip/2.0/udp 192.0.2.1:5060;branch=z9hG4bK-lower\n"
        "max-forwards: 70\n"
        "from: <sip:alice@example.com>;tag=a1\n"
        "to: <sip:bob@example.com>\n"
        "call-id: sipdrift-lower@example.com\n"
        "cseq: 1 invite\n"
        "content-length: 0\n\n",
    ),
    "F-SPACES-START": (
        "spaces_start.sip",
        "SIP/2.0  200  OK\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-spaces\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-spaces@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-TAB-SEP": (
        "tab_sep_headers.sip",
        "OPTIONS sip:bob@example.com SIP/2.0\n"
        "Via:\tSIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-tab\n"
        "Max-Forwards:\t70\n"
        "From:\t<sip:alice@example.com>;tag=a1\n"
        "To:\t<sip:bob@example.com>\n"
        "Call-ID:\tsipdrift-tab@example.com\n"
        "CSeq:\t1 OPTIONS\n"
        "Content-Length:\t0\n\n",
    ),
    "F-UNKNOWN-METHOD": (
        "unknown_method.sip",
        "FOOBAR sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-foobar\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-foobar@example.com\n"
        "CSeq: 1 FOOBAR\n"
        "Content-Length: 0\n\n",
    ),
    "F-NO-HEADERS": (
        "no_headers.sip",
        "SIP/2.0 200 OK\n\n",
    ),
    "F-ONLY-START": (
        "only_start_line.sip",
        "OPTIONS sip:bob@example.com SIP/2.0\n",
    ),
    "F-JUNK-AFTER": (
        "junk_after_message.sip",
        "SIP/2.0 200 OK\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-junk\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-junk@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n"
        "JUNK-TRAILER-NOT-SIP\n",
    ),
    "F-MISSING-VIA": (
        "missing_via.sip",
        "INVITE sip:bob@example.com SIP/2.0\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-novia@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
    "F-MISSING-CSEQ": (
        "missing_cseq.sip",
        "INVITE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-nocseq\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-nocseq@example.com\n"
        "Content-Length: 0\n\n",
    ),
    "F-BAD-STATUS": (
        "bad_status_code.sip",
        "SIP/2.0 999 Weird\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-999\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-999@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Length: 0\n\n",
    ),
}


def main() -> None:
    FIX.mkdir(parents=True, exist_ok=True)
    index_lines = []
    for fid, (name, body) in CASES.items():
        path = FIX / name
        wire = body.replace("\n", "\r\n")
        path.write_bytes(wire.encode("utf-8"))
        index_lines.append(f'    "{fid}": "{name}",')
        print(f"wrote {fid} -> {name}")
    print("--- paste into FIXTURE_INDEX ---")
    print("\n".join(index_lines))


if __name__ == "__main__":
    main()
