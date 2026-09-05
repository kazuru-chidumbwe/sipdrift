# Known divergences

Honest record of cross-stack divergences under pinned fixtures.

**Last updated:** 2026-09-05 · **Harness:** `0.3.3` · **Oracle axes:** `start_line`, `status_code`, `via`, `cseq`, `content_type`, `content_length`, `body_sha256`, `sdp_sha256`  
**Lab pack:** `sipdrift-hostb-20260905T015940Z` · **Corpus:** 53 fixtures · **Drivers:** 7 (incl. Kamailio)

## Stub-tier

| Pair | agree | diverge | error |
| --- | ---: | ---: | ---: |
| `builtin` / `*-stub` pairs | 52 | 0 | 1 |

## Lab-tier headlines (pack `…015940Z`)

| Pair | agree | diverge | error |
| --- | ---: | ---: | ---: |
| `builtin` vs `sofia-lab` | 49 | 3 | 1 |
| `pjsip-lab` vs `sofia-lab` | 48 | 1 | 4 |
| `builtin` vs `kamailio-lab` | 41 | 6 | 6 |
| `sofia-lab` vs `kamailio-lab` | 41 | 6 | 6 |
| `pjsip-lab` vs `kamailio-lab` | 41 | 5 | 7 |

## UA-library divergences

| Fixture | Pair | Notes |
| --- | --- | --- |
| `F-FOLDED-VIA` | builtin vs sofia-lab | Fold unfold |
| `F-LOWER-SIP` | builtin / pjsip vs sofia | Case / version normalize |
| `F-SPACES-START` | builtin vs sofia-lab | Status whitespace |
| `F-TORTURE-UNKNOWN-SCHEME` | pjsip-lab | Parse error on unknown URI scheme |

## Body / SDP

SDP and plain-body fixtures (`F-INVITE-SDP`, `F-200-SDP`, `F-SDP-TRAIL-WS`, `F-COMPACT-CTYPE`, `F-MESSAGE-BODY`) **agree** across stub pairs and UA labs under wire-body fingerprint axes. `body_sha256` and `sdp_sha256` differ when SDP has trailing whitespace (by design).

## Kamailio proxy-tier

| Fixture | Typical status | Notes |
| --- | --- | --- |
| Happy-path + SDP bodies | **agree** with library labs on many axes | UDP receive + Lua dump; body axes from wire |
| `F-FOLDED-VIA` | **diverge** | May retain folded whitespace in Via value |
| `F-LOWER-SIP` | **diverge** | Method/Via case policy differs |
| `F-TORTURE-WS-END` · `F-TORTURE-DUP-VIA` · `F-TORTURE-MULTI-CLEN` | **diverge** | Via extraction / receive oddities |
| `F-TORTURE-UNKNOWN-SCHEME` | **diverge** | Empty Request-URI after scheme reject |
| Incomplete / missing required headers | **error** | Proxy receive path |

## Live OPTIONS

default / `--all` / `--1XX` → **rc=0**.
