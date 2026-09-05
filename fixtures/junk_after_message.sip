SIP/2.0 200 OK
Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-junk
From: <sip:alice@example.com>;tag=a1
To: <sip:bob@example.com>;tag=b1
Call-ID: sipdrift-junk@example.com
CSeq: 1 INVITE
Content-Length: 0

JUNK-TRAILER-NOT-SIP
