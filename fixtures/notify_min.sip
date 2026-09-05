NOTIFY sip:alice@example.com SIP/2.0
Via: SIP/2.0/UDP 192.0.2.2:5060;branch=z9hG4bK-notify
Max-Forwards: 70
From: <sip:bob@example.com>;tag=b1
To: <sip:alice@example.com>;tag=a1
Call-ID: sipdrift-notify@example.com
CSeq: 1 NOTIFY
Event: presence
Subscription-State: active
Content-Length: 0

