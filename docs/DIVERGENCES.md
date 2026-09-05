# Known divergences

Honest record of cross-stack divergences under pinned fixtures.

**Last updated:** 2026-09-05 · **Harness:** `0.3.1` · **Oracle axes:** `start_line`, `status_code`, `via`, `cseq`  
**Lab pack:** `sipdrift-hostb-20260905T012008Z` (Host B `10.4.0.32`) · **Corpus:** 40 fixtures

## Stub-tier runs (parse-path)

| Fixture pair | Left | Right | Status | Notes |
| --- | --- | --- | --- | --- |
| Corpus × stubs | `builtin` | `pjsip-stub` / `sofia-stub` | **39 agree · 1 error** | `F-MALFORMED-START` errors both sides |
| OSS stub pair | `pjsip-stub` | `sofia-stub` | **39 agree · 1 error** | Shared parse-path axes |

## Lab-tier runs (Host B)

### `builtin` vs `sofia-lab` — **35 agree · 4 diverge · 1 error**

| Fixture | Status | Notes |
| --- | --- | --- |
| `F-COMPACT-VIA` | **diverge** | Builtin misses compact `v:`; Sofia expands Via |
| `F-FOLDED-VIA` | **diverge** | Builtin keeps folded first line; Sofia unfolds branch |
| `F-LOWER-SIP` | **diverge** | Sofia normalizes `sip/2.0` → `SIP/2.0` |
| `F-SPACES-START` | **diverge** | Sofia collapses `SIP/2.0  200  OK` → `SIP/2.0 200 OK` |
| `F-MALFORMED-START` | **error** | Both fail (expected) |
| Torture subset (8) | **agree** (vs sofia-lab) | LWS/escaped/long-URI/clen/dup/nonascii/null/ws-end parsed consistently enough for axes |

### `pjsip-lab` vs `sofia-lab` — **36 agree · 1 diverge · 3 error**

| Fixture | Status | Notes |
| --- | --- | --- |
| `F-LOWER-SIP` | **diverge** | PJSIP uppercases method/`INVITE`; Sofia preserves `invite` |
| `F-MALFORMED-START` · `F-NO-HEADERS` · `F-ONLY-START` | **error** | Incomplete messages — one or both parsers reject |

### `builtin` vs `pjsip-lab` — **33 agree · 4 diverge · 3 error**

Same normalization-class divergences as sofia-lab on compact/folded/lower/spaces, plus incomplete-message errors.

## Live OPTIONS (fixed in 0.3.1)

Responder: `0.0.0.0:15060`. Client: `sip-options -m sip:127.0.0.1:15061 sip:127.0.0.1:15060`.

| Probe | rc |
| --- | ---: |
| default | **0** |
| `--all` | **0** |
| `--1XX` | **0** |

## Taxonomy

| Status | Meaning |
| --- | --- |
| agree | All oracle axes match |
| diverge | One or more axes differ |
| error | One or both drivers failed |
| skip | Driver or axis unavailable |

Lab divergences are **normalization differences**, not necessarily bugs. They are the research product of the differential oracle.
