# Fixture corpus

Pinned SIP message snippets for differential runs (CRLF wire).

| ID | File | Intent |
| --- | --- | --- |
| `F-INVITE-MIN` | `invite_min.sip` | Minimal INVITE |
| `F-200-MIN` | `response_200_min.sip` | 200 OK |
| `F-486-MIN` | `response_486_busy.sip` | 486 Busy Here |
| `F-503-MIN` | `response_503_unavail.sip` | 503 Service Unavailable |
| `F-OPTIONS-MIN` | `options_min.sip` | OPTIONS |
| `F-REGISTER-MIN` | `register_min.sip` | REGISTER |
| `F-MALFORMED-START` | `malformed_start.sip` | Empty / missing start-line |
| `F-100-TRYING` | `response_100_trying.sip` | 100 Trying |
| `F-180-RINGING` | `response_180_ringing.sip` | 180 Ringing |
| `F-401-AUTH` | `response_401_auth.sip` | 401 Unauthorized |
| `F-404-NOTFOUND` | `response_404_notfound.sip` | 404 Not Found |
| `F-603-DECLINE` | `response_603_decline.sip` | 603 Decline |
| `F-ACK-MIN` / `F-BYE-MIN` / `F-CANCEL-MIN` | `*_min.sip` | Dialog methods |
| `F-INFO-MIN` / `F-MESSAGE-MIN` | … | Mid-dialog / pager |
| `F-NOTIFY-MIN` / `F-SUBSCRIBE-MIN` | … | Event package |
| `F-COMPACT-VIA` | `compact_via.sip` | Compact form headers |
| `F-MULTI-VIA` | `multi_via.sip` | Multiple Via |
| `F-FOLDED-VIA` | `folded_via.sip` | Folded header continuation |
| `F-LOWER-SIP` | `lower_sip_version.sip` | Lower-case start-line |
| `F-SPACES-START` | `spaces_start.sip` | Extra spaces in status line |
| `F-TAB-SEP` | `tab_sep_headers.sip` | Tab after colon |
| `F-UNKNOWN-METHOD` | `unknown_method.sip` | Non-standard method |
| `F-NO-HEADERS` / `F-ONLY-START` | … | Incomplete messages |
| `F-JUNK-AFTER` | `junk_after_message.sip` | Trailer junk |
| `F-MISSING-VIA` / `F-MISSING-CSEQ` | … | Required-header absences |
| `F-BAD-STATUS` | `bad_status_code.sip` | Non-standard 999 |
| `F-TORTURE-*` | `torture_*.sip` | RFC 4475–inspired edges (LWS, escaped URI, long URI, bad Content-Length, dup Via/CSeq, non-ASCII Warning, NUL body) |

Regenerate: `python tools/gen_extra_fixtures.py && python tools/gen_torture_fixtures.py && python tools/normalize_fixtures.py`
