#!/usr/bin/env python3
"""Minimal UDP SIP responder for sip-options live experiments."""

from __future__ import annotations

import argparse
import socket


def build_200(req: bytes) -> bytes:
    text = req.decode("utf-8", errors="replace")
    via = "Via: SIP/2.0/UDP 127.0.0.1"
    cseq = "CSeq: 1 OPTIONS"
    call_id = "Call-ID: sipdrift-live@127.0.0.1"
    from_h = "From: <sip:probe@127.0.0.1>;tag=sipdrift"
    to_h = "To: <sip:target@127.0.0.1>;tag=lab"
    for line in text.replace("\r\n", "\n").split("\n"):
        low = line.lower()
        if low.startswith("via:"):
            via = line.strip()
        elif low.startswith("cseq:"):
            cseq = line.strip()
        elif low.startswith("call-id:") or low.startswith("i:"):
            call_id = line.strip() if not low.startswith("i:") else f"Call-ID:{line.split(':', 1)[1]}"
        elif low.startswith("from:") or low.startswith("f:"):
            from_h = line.strip() if not low.startswith("f:") else f"From:{line.split(':', 1)[1]}"
        elif low.startswith("to:") or low.startswith("t:"):
            to_h = line.strip() if not low.startswith("t:") else f"To:{line.split(':', 1)[1]};tag=lab"
    body = (
        "SIP/2.0 200 OK\r\n"
        f"{via}\r\n"
        f"{from_h}\r\n"
        f"{to_h}\r\n"
        f"{call_id}\r\n"
        f"{cseq}\r\n"
        "Content-Length: 0\r\n"
        "\r\n"
    )
    return body.encode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=15060)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.host, args.port))
    print(f"sip_udp_responder listening on {args.host}:{args.port}", flush=True)
    while True:
        data, addr = sock.recvfrom(65535)
        if not data:
            continue
        sock.sendto(build_200(data), addr)


if __name__ == "__main__":
    raise SystemExit(main())
