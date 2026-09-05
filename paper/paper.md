---
title: 'sipdrift: A Differential Testing Harness for Open-Source SIP Stacks'
tags:
  - SIP
  - VoIP
  - differential testing
  - interoperability
  - security
  - Python
authors:
  - name: Seke Kazuru
    orcid: 0009-0002-4099-1059
    affiliation: "1"
affiliations:
  - name: Independent Researcher
    index: 1
date: 5 September 2026
bibliography: paper.bib
---

# Summary

Session Initiation Protocol (SIP) stacks are the control-plane substrate for Voice over IP (VoIP), unified communications, and many telecom edge deployments [@rfc3261]. Open-source implementations — notably PJSIP [@pjsip], Sofia-SIP [@sofia], and Kamailio-class proxies [@kamailio] — are routinely combined in production platforms and research testbeds. Interoperability defects and semantic divergences between stacks are a recurring source of mis-routing, toll-fraud exposure, and security bypasses that single-stack conformance suites do not surface.

**sipdrift** is an open-source differential testing harness for SIP message handling. It runs a pinned corpus of SIP fixtures through multiple stack drivers, normalizes each driver's observations onto shared oracle axes (start-line, status code, Via, CSeq), and classifies each fixture as `agree`, `diverge`, `error`, or `skip`. The harness ships a Python package with a `StackDriver` protocol, stub and lab drivers for PJSIP and Sofia-SIP, a `compare`/`suite` CLI with text and JSON reports, GitHub Actions continuous integration, and a JOSS-oriented paper pack under `paper/`.

# Statement of need

Production VoIP platforms assemble SIP proxies, media servers, session border controllers, and edge firewalls from different vendors and OSS projects. RFC 3261 conformance is necessary but not sufficient: stacks diverge on compact-form headers, folded header lines, whitespace tolerance, escaped URIs, unknown methods, and incomplete messages [@rfc3261; @rfc4475]. Those divergences matter for operators who must reason about what a peer will accept or rewrite, and for researchers studying protocol robustness and defence-in-depth at the signalling layer.

Existing SIP tooling clusters into four useful but incomplete categories:

1. **Load / scenario tools** such as SIPp generate traffic against a single target [@sipp].
2. **Interop events** such as SIPit expose live multi-vendor behaviour but are not a reproducible fixture corpus [@sipit].
3. **Single-stack unit and conformance tests** validate one implementation in isolation.
4. **Protocol fuzzers** find crashes and assertion failures but rarely emit a structured cross-stack agreement classification [@afl; @resolfuzz; @resolverfuzz].

sipdrift fills the gap with a **repeatable differential oracle**: identical fixtures, multiple drivers, shared axes, and machine-readable outcomes. The design follows the same fixture-driven differential pattern used in related network-stack measurement work, specialised here to SIP message observation rather than live call completion or DNS path consistency.

Who benefits:

- **Operators** comparing candidate SIP stacks or upgrades under controlled inputs before cut-over.
- **Security researchers** documenting parser and header-handling drift that can enable request-smuggling or auth-bypass hypotheses.
- **OSS maintainers** adding regression fixtures when a divergence is fixed or accepted as intentional.

# Methodology and architecture

## Pipeline

```text
fixture (.sip) → StackDriver.observe() × N → classify_observations() → report
```

| Layer | Module | Role |
| --- | --- | --- |
| Fixtures | `fixtures/*.sip` | Pinned SIP inputs (CRLF wire; stable IDs) |
| Parse | `sipdrift.parse` | Reference start-line and header extraction |
| Drivers | `sipdrift.drivers` | `StackDriver` implementations per stack tier |
| Harness | `sipdrift.harness` | Multi-axis classification oracle |
| Run loop | `sipdrift.run` | Load → observe ×2 → classify → report |
| CLI | `sipdrift.cli` | `status`, `fixtures`, `drivers`, `compare`, `suite` |
| Lab tools | `tools/sofia_observe`, `tools/pjsip_observe` | Subprocess adapters for real OSS parsers |

## Oracle axes

From **0.2.0**, the default oracle compares:

| Axis | Meaning |
| --- | --- |
| `start_line` | First non-empty request or status line |
| `status_code` | Numeric response code when present |
| `via` | First Via header value |
| `cseq` | CSeq header value |

Outcomes: `agree` · `diverge` · `error` · `skip`.

## Driver tiers

| Driver | Tier | Backend |
| --- | --- | --- |
| `builtin` | Reference | Pure-Python parse path (not an OSS SIP stack) |
| `pjsip-stub` / `sofia-stub` | Stub | Same parse path; documents intended OSS targets |
| `pjsip-lab` | Lab | `tools/pjsip_observe` (`pjsip_parse_msg`) |
| `sofia-lab` | Lab | `tools/sofia_observe` (Sofia `msg_make`) |

CI exercises stub and reference drivers so the package remains installable without native SIP libraries. Lab drivers are optional and host-pinned.

## Fixture corpus

Version **0.3.1** ships **40** fixtures: happy-path requests/responses, dialog methods, event packages, compact/folded/multi-Via, case and whitespace edges, incomplete messages, and an RFC 4475–inspired torture subset (LWS around colons, escaped URIs, long URI user parts, mismatched Content-Length, duplicate Via/CSeq, non-ASCII Warning text, NUL-in-body claims).

## Threats to validity

- Drivers observe **parse/normalization** of a fixture blob — not full transaction or media state machines.
- Normalization differences are real under the chosen axes, but may be intentional stack policy.
- Lab binaries are host-pinned; reproducers without Sofia/PJSIP fall back to stubs.
- Kamailio proxy-tier observation is scoped but not implemented [@kamailio] — see `docs/KAMAILIO-SCOPE.md`.

# State of the field

| Approach | Strength | Gap vs sipdrift |
| --- | --- | --- |
| SIPp scenarios [@sipp] | Scalable load, scripted call flows | Single-target; no multi-stack normalized oracle |
| SIPit / interop events [@sipit] | Live multi-vendor exposure | Not a pinned, replayable corpus |
| RFC 4475 torture tests [@rfc4475] | Canonical hard cases | Usually applied one stack at a time |
| Differential DNS fuzzing [@resolfuzz; @resolverfuzz] | Semantic diverge discovery | DNS, not SIP message fixtures |
| Project-local test suites | Deep coverage for one stack | Not cross-stack by construction |

sipdrift asks: *do these stacks agree on these axes under this input?*

# Results

## Lab setup

Ephemeral Host B (`10.4.0.32`, Ubuntu 24.04, 16 vCPU). Sofia-SIP `1.12.11` from distro packages; PJSIP built from upstream pjproject. Packs written under `/opt/atlas/sipdrift-packs/`. Canonical Results pack: **`sipdrift-hostb-20260905T012008Z`** (`0.3.1`, 40 fixtures, live OPTIONS fixed).

## Experiment classes

1. Full-corpus **driver-pair suites** (all ordered pairs among five drivers).
2. Per-fixture **builtin vs sofia-lab** spotlights.
3. Sofia CLI tool smokes (`sip-date`, `localinfo`, `addrinfo`, `sip-dig`, `sip-options`, `stunc`).
4. **Live OPTIONS** via UDP responder + Sofia `sip-options` (`-m sip:127.0.0.1:15061` → `sip:127.0.0.1:15060`).
5. **pytest** on the lab virtualenv.

## Headline suite outcomes (0.3.1 pack `sipdrift-hostb-20260905T012008Z`, 40 fixtures)

| Pair | agree | diverge | error |
| --- | ---: | ---: | ---: |
| Stub pairs (`builtin` / `pjsip-stub` / `sofia-stub`) | 39 | 0 | 1 |
| `builtin` vs `sofia-lab` | 35 | 4 | 1 |
| `pjsip-lab` vs `sofia-lab` | 36 | 1 | 3 |
| `builtin` vs `pjsip-lab` | 33 | 4 | 3 |

The single stub-tier error is `F-MALFORMED-START` (expected). Torture fixtures (8) did not add new sofia-lab diverge rows beyond the four normalization cases above.

## Notable divergences

| Fixture | Pair | Axis behaviour |
| --- | --- | --- |
| `F-COMPACT-VIA` | builtin vs sofia-lab | Builtin misses compact `v:`; Sofia expands Via |
| `F-FOLDED-VIA` | builtin vs sofia-lab | Builtin keeps folded fragment; Sofia unfolds `branch` |
| `F-LOWER-SIP` | builtin vs sofia-lab | Sofia normalizes `sip/2.0` → `SIP/2.0` |
| `F-SPACES-START` | builtin vs sofia-lab | Sofia collapses extra spaces in status line |
| `F-LOWER-SIP` | pjsip-lab vs sofia-lab | PJSIP uppercases method; Sofia preserves `invite` |

## Live OPTIONS

With the responder bound on `0.0.0.0:15060` and `sip-options` using a distinct local bind URL on port `15061`, Host B returns `SIP/2.0 200 OK` for default, `--all`, and `--1XX` probes (**rc=0**). This is complementary to fixture differential runs — not a claim about production SBCs.

# Reproducibility and smoke gate

## Install (stub / CI path)

```bash
git clone https://github.com/kazuru-chidumbwe/sipdrift.git
cd sipdrift
python -m pip install -e ".[dev]"
python -m pytest -q
python -m sipdrift.cli compare F-200-MIN
python -m sipdrift.cli suite --right sofia-stub
```

Expected: `compare` exit **0** (`agree`); `suite` exit **1** when the malformed fixture errors (remaining stub-pair cases agree).

See also `examples/README.md`.

## Lab path (optional)

```bash
cd tools && make sofia
export SIPDRIFT_SOFIA_OBSERVE=$PWD/sofia_observe
python -m sipdrift.cli suite --left builtin --right sofia-lab

cd tools && make pjsip PJDIR=/path/to/pjproject
export SIPDRIFT_PJSIP_OBSERVE=$PWD/pjsip_observe
python -m sipdrift.cli suite --left pjsip-lab --right sofia-lab
python tools/run_hostb_experiments.py
```

## Continuous integration

GitHub Actions (`.github/workflows/ci.yml`) runs `pytest` on pushes and pull requests to `main`.

# Acknowledgements

Thanks to maintainers of PJSIP and Sofia-SIP for open libraries that make lab drivers possible, and to operators who share SIP edge-case traces that inform fixture design.

## AI usage disclosure

Drafting and refactoring of harness code and this manuscript were assisted by AI coding tools under author direction. All experimental claims, fixture contents, oracle definitions, and final wording were reviewed and accepted by the author. No AI system is listed as an author or contributor.

# References
