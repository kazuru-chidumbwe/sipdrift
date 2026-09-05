OPTIONS sip:bob@example.com SIP/2.0
Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-unrecog
Max-Forwards: 70
From: <sip:alice@example.com>;tag=a1
To: <sip:bob@example.com>
Call-ID: sipdrift-unrecog@example.com
CSeq: 1 OPTIONS
X-Sipdrift-Odd: yes-please
Content-Length: 0

