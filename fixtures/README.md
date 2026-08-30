# Fixture corpus

Pinned SIP message snippets for differential runs.

| ID | File | Intent |
| --- | --- | --- |
| `F-INVITE-MIN` | `invite_min.sip` | Minimal INVITE request start + Via |
| `F-200-MIN` | `response_200_min.sip` | Minimal 200 OK response |
| `F-486-MIN` | `response_486_busy.sip` | 4xx — 486 Busy Here |
| `F-503-MIN` | `response_503_unavail.sip` | 5xx — 503 Service Unavailable |
| `F-OPTIONS-MIN` | `options_min.sip` | OPTIONS request |
| `F-REGISTER-MIN` | `register_min.sip` | REGISTER request |
| `F-MALFORMED-START` | `malformed_start.sip` | Missing start-line (ERROR path) |

**Rules (honest scaffold):**

- Fixtures are **inputs only** — no claim that any stack under test matches them.
- Prefer CRLF line endings in `.sip` files (SIP wire convention).
- Do not invent stack behaviour in fixtures; expand corpus when a real compare case lands.
