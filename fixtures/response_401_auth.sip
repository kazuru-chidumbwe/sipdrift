SIP/2.0 401 Unauthorized
Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-401
From: <sip:alice@example.com>;tag=a1
To: <sip:bob@example.com>;tag=b1
Call-ID: sipdrift-401@example.com
CSeq: 1 REGISTER
WWW-Authenticate: Digest realm="example.com", nonce="abc"
Content-Length: 0

