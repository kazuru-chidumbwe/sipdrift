# Known divergences

Honest record of cross-stack divergences under pinned fixtures.

**Last updated:** 2026-09-05 · **Harness:** `0.3.0` · **Oracle axes:** `start_line`, `status_code`, `via`, `cseq`  
**Lab pack:** `sipdrift-hostb-20260905T010835Z` (Host B `10.4.0.32`)

## Stub-tier runs (parse-path)

| Fixture pair | Left | Right | Status | Notes |
| --- | --- | --- | --- | --- |
| Corpus × default | `builtin` | `pjsip-stub` / `sofia-stub` | **31 agree · 1 error** | Malformed start errors both sides |
| OSS stub pair | `pjsip-stub` | `sofia-stub` | **31 agree · 1 error** | Shared parse-path axes |

## Lab-tier runs (Host B)

### `builtin` vs `sofia-lab`

| Fixture | Status | Notes |
| --- | --- | --- |
| `F-COMPACT-VIA` | **diverge** | Builtin misses compact `v:`; Sofia expands Via |
| `F-FOLDED-VIA` | **diverge** | Builtin keeps folded first line; Sofia unfolds branch |
| `F-LOWER-SIP` | **diverge** | Sofia normalizes `sip/2.0` → `SIP/2.0` in Via/start |
| `F-SPACES-START` | **diverge** | Sofia collapses `SIP/2.0  200  OK` → `SIP/2.0 200 OK` |
| `F-MALFORMED-START` | **error** | Both fail (expected) |
| Remaining | **agree** | — |

### `pjsip-lab` vs `sofia-lab`

| Fixture | Status | Notes |
| --- | --- | --- |
| `F-LOWER-SIP` | **diverge** | PJSIP uppercases method/`INVITE`; Sofia preserves `invite` on start/CSeq |
| `F-MALFORMED-START` · `F-NO-HEADERS` · `F-ONLY-START` | **error** | Incomplete messages — one or both parsers reject |
| Remaining | **agree** (28) | Shared normalized axes on happy-path + most edges |

## Taxonomy

| Status | Meaning |
| --- | --- |
| agree | All oracle axes match |
| diverge | One or more axes differ |
| error | One or both drivers failed |
| skip | Driver or axis unavailable |

Lab divergences are **normalization differences**, not necessarily bugs. They are the research product of the differential oracle.
