# Known divergences

Honest record of cross-stack divergences under pinned fixtures.

**Last updated:** 2026-09-05 · **Harness:** `0.3.2` · **Oracle axes:** `start_line`, `status_code`, `via`, `cseq`  
**Lab pack:** `sipdrift-hostb-20260905T012956Z` (Host B `10.4.0.32`) · **Corpus:** 40 fixtures · **Drivers:** 7 (incl. Kamailio)

## Stub-tier

| Pair | agree | diverge | error |
| --- | ---: | ---: | ---: |
| `builtin` / `*-stub` pairs | 39 | 0 | 1 |

## Lab-tier headlines (pack `…012956Z`)

| Pair | agree | diverge | error |
| --- | ---: | ---: | ---: |
| `builtin` vs `sofia-lab` | 35 | 4 | 1 |
| `pjsip-lab` vs `sofia-lab` | 36 | 1 | 3 |
| `builtin` vs `kamailio-lab` | 29 | 5 | 6 |
| `sofia-lab` vs `kamailio-lab` | 30 | 4 | 6 |
| `pjsip-lab` vs `kamailio-lab` | 30 | 4 | 6 |

## UA-library divergences (unchanged class)

| Fixture | Pair | Notes |
| --- | --- | --- |
| `F-COMPACT-VIA` | builtin vs sofia-lab | Compact `v:` expansion |
| `F-FOLDED-VIA` | builtin vs sofia-lab | Fold unfold |
| `F-LOWER-SIP` | builtin / pjsip vs sofia | Case / version normalize |
| `F-SPACES-START` | builtin vs sofia-lab | Status whitespace |

## Kamailio proxy-tier (new in 0.3.2)

| Fixture | Typical status | Notes |
| --- | --- | --- |
| Happy-path requests | **agree** with library labs on many axes | UDP receive + Lua dump |
| `F-COMPACT-VIA` | **diverge** vs builtin | Kamailio expands compact Via (like Sofia) |
| `F-FOLDED-VIA` | **diverge** vs pjsip/sofia | Kamailio may retain folded whitespace in Via value |
| `F-LOWER-SIP` | **diverge** | Method/Via case policy differs across stacks |
| `F-SPACES-START` · `F-NO-HEADERS` · `F-ONLY-START` · `F-MALFORMED-START` | **error** | Incomplete / odd messages often rejected on proxy receive path |

## Live OPTIONS

default / `--all` / `--1XX` → **rc=0** (unchanged from 0.3.1).
