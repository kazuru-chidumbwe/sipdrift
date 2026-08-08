# Fixture corpus (scaffold)

Pinned SIP message snippets for differential runs.

| ID | File | Intent |
| --- | --- | --- |
| `F-INVITE-MIN` | `invite_min.sip` | Minimal INVITE request start + Via |
| `F-200-MIN` | `response_200_min.sip` | Minimal 200 OK response |

**Rules (honest scaffold):**

- Fixtures are **inputs only** — no claim that any stack under test matches them.
- Prefer CRLF line endings in `.sip` files (SIP wire convention).
- Do not invent stack behaviour in fixtures; expand corpus when a real compare case lands.
