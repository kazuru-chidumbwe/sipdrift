INVITE sip:bob@example.com SIP/2.0
Via: SIP/2.0/UDP 192.0.2.1:5060;branch=z9hG4bK-invite-sdp
Max-Forwards: 70
From: <sip:alice@example.com>;tag=a1
To: <sip:bob@example.com>
Call-ID: sipdrift-invite-sdp@example.com
CSeq: 1 INVITE
Contact: <sip:alice@192.0.2.1:5060>
Content-Type: application/sdp
Content-Length: 139

v=0
o=alice 2890844526 2890844526 IN IP4 192.0.2.1
s=sipdrift
c=IN IP4 192.0.2.1
t=0 0
m=audio 49170 RTP/AVP 0
a=rtpmap:0 PCMU/8000
