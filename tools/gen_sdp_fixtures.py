#!/usr/bin/env python3
"""Generate SDP / body oracle fixtures."""

from __future__ import annotations

from pathlib import Path

FIX = Path(__file__).resolve().parents[1] / "fixtures"

_SDP = (
    "v=0\n"
    "o=alice 2890844526 2890844526 IN IP4 192.0.2.1\n"
    "s=sipdrift\n"
    "c=IN IP4 192.0.2.1\n"
    "t=0 0\n"
    "m=audio 49170 RTP/AVP 0\n"
    "a=rtpmap:0 PCMU/8000\n"
)

_SDP_WS = (
    "v=0  \n"
    "o=alice 2890844526 2890844526 IN IP4 192.0.2.1\n"
    "s=sipdrift\n"
    "c=IN IP4 192.0.2.1\n"
    "t=0 0\n"
    "m=audio 49170 RTP/AVP 0\n"
    "a=rtpmap:0 PCMU/8000\n"
    "\n"
)

CASES: dict[str, tuple[str, str]] = {
    "F-INVITE-SDP": (
        "invite_sdp.sip",
        "INVITE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-invite-sdp\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-invite-sdp@example.com\n"
        "CSeq: 1 INVITE\n"
        "Contact: <sip:alice@192.0.2.1:5060>\n"
        "Content-Type: application/sdp\n"
        f"Content-Length: {len(_SDP.replace(chr(10), chr(13) + chr(10)))}\n\n"
        f"{_SDP}",
    ),
    "F-200-SDP": (
        "response_200_sdp.sip",
        "SIP/2.0 200 OK\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-200-sdp\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>;tag=b1\n"
        "Call-ID: sipdrift-200-sdp@example.com\n"
        "CSeq: 1 INVITE\n"
        "Contact: <sip:bob@192.0.2.2:5060>\n"
        "Content-Type: application/sdp\n"
        f"Content-Length: {len(_SDP.replace(chr(10), chr(13) + chr(10)))}\n\n"
        f"{_SDP}",
    ),
    "F-SDP-TRAIL-WS": (
        "sdp_trail_ws.sip",
        "INVITE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-sdp-ws\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-sdp-ws@example.com\n"
        "CSeq: 1 INVITE\n"
        "Content-Type: application/sdp\n"
        f"Content-Length: {len(_SDP_WS.replace(chr(10), chr(13) + chr(10)))}\n\n"
        f"{_SDP_WS}",
    ),
    "F-COMPACT-CTYPE": (
        "compact_ctype.sip",
        "INVITE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-c-ctype\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-c-ctype@example.com\n"
        "CSeq: 1 INVITE\n"
        "c: application/sdp\n"
        f"l: {len(_SDP.replace(chr(10), chr(13) + chr(10)))}\n\n"
        f"{_SDP}",
    ),
    "F-MESSAGE-BODY": (
        "message_body.sip",
        "MESSAGE sip:bob@example.com SIP/2.0\n"
        "Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-msg-body\n"
        "Max-Forwards: 70\n"
        "From: <sip:alice@example.com>;tag=a1\n"
        "To: <sip:bob@example.com>\n"
        "Call-ID: sipdrift-msg-body@example.com\n"
        "CSeq: 1 MESSAGE\n"
        "Content-Type: text/plain\n"
        "Content-Length: 11\n\n"
        "hello world",
    ),
}


def main() -> None:
    FIX.mkdir(parents=True, exist_ok=True)
    for fid, (name, body) in CASES.items():
        path = FIX / name
        # Fix Content-Length after CRLF conversion
        wire_lf = body
        # Recompute length for SDP cases accurately
        if "\n\n" in wire_lf:
            headers, _, payload = wire_lf.partition("\n\n")
            payload_crlf = payload.replace("\n", "\r\n")
            # Rewrite Content-Length / l: lines
            new_headers: list[str] = []
            for line in headers.split("\n"):
                low = line.lower()
                if low.startswith("content-length:"):
                    new_headers.append(f"Content-Length: {len(payload_crlf.encode('utf-8'))}")
                elif low.startswith("l:"):
                    new_headers.append(f"l: {len(payload_crlf.encode('utf-8'))}")
                else:
                    new_headers.append(line)
            wire = ("\r\n".join(new_headers) + "\r\n\r\n").encode("utf-8") + payload_crlf.encode(
                "utf-8"
            )
        else:
            wire = wire_lf.replace("\n", "\r\n").encode("utf-8")
        path.write_bytes(wire)
        print(f"wrote {fid} -> {name}")


if __name__ == "__main__":
    main()
