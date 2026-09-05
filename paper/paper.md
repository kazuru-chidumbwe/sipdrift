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

Session Initiation Protocol (SIP) stacks are the control-plane substrate for Voice over IP (VoIP), unified communications, and many telecom edge deployments [@rfc3261]. Open-source implementations — notably PJSIP, Sofia-SIP, and Kamailio-class proxies — are routinely combined in production platforms and research testbeds. Interoperability defects and semantic divergences between stacks are a recurring source of mis-routing, toll-fraud exposure, and security bypasses that single-stack conformance suites do not surface.

**sipdrift** is an open-source differential testing harness for SIP message handling. It runs a pinned corpus of SIP fixtures through multiple stack drivers, normalizes each driver's observations onto shared oracle axes (start-line, status code, Via, CSeq), and classifies each fixture as `agree`, `diverge`, `error`, or `skip`. The harness ships a Python package with a `StackDriver` protocol, stub and lab drivers for PJSIP and Sofia-SIP, a `compare`/`suite` CLI with text and JSON reports, and GitHub Actions continuous integration.

# Statement of need

Production VoIP platforms assemble SIP proxies, media servers, session border controllers, and edge firewalls from different vendors and OSS projects. RFC 3261 conformance is necessary but not sufficient: stacks diverge on compact-form headers, folded header lines, whitespace tolerance, unknown methods, and incomplete messages [@rfc3261; @rfc4475]. Those divergences matter for operators who must reason about what a peer will accept or rewrite, and for researchers studying protocol robustness and defence-in-depth at the signalling layer.

Existing SIP tooling clusters into four useful but incomplete categories:

1. **Load / scenario tools** such as SIPp generate traffic against a single target [@sipp].
2. **Interop events** such as SIPit expose live multi-vendor behaviour but are not a reproducible fixture corpus [@sipit].
3. **Single-stack unit and conformance tests** validate one implementation in isolation.
4. **Protocol fuzzers** find crashes and assertion failures but rarely emit a structured cross-stack agreement classification [@afl; @resolfuzz].

sipdrift fills the gap with a **repeatable differential oracle**: identical fixtures, multiple drivers, shared axes, and machine-readable outcomes. The design follows the same fixture-driven differential pattern used in related network and credential-stack measurement work (DNS StackDiff; eMRTD differential harnesses), specialised here to SIP message observation rather than live call completion.

Who benefits:

- **Operators** comparing candidate SIP stacks or upgrades under controlled inputs before cut-over.
- **Security researchers** documenting parser and header-handling drift that can enable request smuggling or auth bypass hypotheses.
- **OSS maintainers** adding regression fixtures when a divergence is fixed or accepted as intentional.

# Methodology and architecture

## Pipeline

```text
fixture (.sip) → StackDriver.observe() × N → classify_observations() → report
```

| Layer | Module | Role |
| --- | --- | --- |
| Fixtures | `fixtures/*.sip` | Pinned SIP inputs (CRLF wire convention; stable IDs) |
| Parse | `sipdrift.parse` | Reference start-line and header extraction |
| Drivers | `sipdrift.drivers` | `StackDriver` implementations per stack tier |
| Harness | `sipdrift.harness` | Multi-axis classification oracle |
| Run loop | `sipdrift.run` | Load → observe ×2 → classify → report |
| CLI | `sipdrift.cli` | `status`, `fixtures`, `drivers`, `compare`, `suite` |
| Lab tools | `tools/sofia_observe`, `tools/pjsip_observe` | Subprocess adapters for real OSS parsers |

## Oracle axes

Phase 1 compared start-lines only. From **0.2.0**, the default oracle compares:

| Axis | Meaning |
| --- | --- |
| `start_line` | First non-empty request or status line |
| `status_code` | Numeric response code when present |
| `via` | First Via header value |
| `cseq` | CSeq header value |

Outcomes:

| Status | Meaning |
| --- | --- |
| `agree` | All compared axes match and both observations succeeded |
| `diverge` | Both succeeded but at least one axis differs |
| `error` | One or both observations failed |
| `skip` | Observation unavailable (driver not implemented for an axis) |

## Driver tiers

| Driver | Tier | Backend |
| --- | --- | --- |
| `builtin` | Reference | Pure-Python parse path (not an OSS SIP stack) |
| `pjsip-stub` / `sofia-stub` | Stub | Same parse path; documents intended OSS targets |
| `pjsip-lab` | Lab | Subprocess to `tools/pjsip_observe` (PJSIP `pjsip_parse_msg`) |
| `sofia-lab` | Lab | Subprocess to `tools/sofia_observe` (Sofia-SIP `msg_make`) |

Lab drivers are intended for Lab Test Server / Host B runs where PJSIP and Sofia-SIP are installed. CI continues to exercise stub and reference drivers so the package remains installable without native SIP libraries.

## Fixture corpus

The corpus mixes minimal happy-path messages with adversarial and edge cases: provisional and final responses, compact-form headers, folded Via, multi-Via, lower-case start-lines, tab-separated headers, unknown methods, missing Via/CSeq, junk trailers, and empty/malformed starts. Fixture IDs (e.g. `F-200-MIN`, `F-COMPACT-VIA`) are stable for regression and paper tables.

## Threats to validity

- **Observation ≠ full stack behaviour.** Drivers currently observe parse/normalization of a fixture blob; they do not yet exercise transaction state machines or media.
- **Normalization differences are real divergences** under the chosen axes, but may be intentional stack policy rather than bugs.
- **Lab binaries are host-pinned.** Reproducers must install matching Sofia-SIP / PJSIP builds or fall back to stub drivers.
- **Corpus bias.** Fixtures emphasise header/start-line edges; SDP bodies and dialog long-runs are future work.

# State of the field

| Approach | Strength | Gap vs sipdrift |
| --- | --- | --- |
| SIPp scenarios [@sipp] | Scalable load, scripted call flows | Single-target; no multi-stack normalized oracle |
| SIPit / interop events [@sipit] | Live multi-vendor exposure | Not a pinned, replayable corpus |
| RFC 4475 torture tests [@rfc4475] | Canonical hard cases | Usually applied one stack at a time |
| Protocol fuzzing [@afl] | Crash discovery | Weak structured agree/diverge reporting |
| Kamailio / FreeSWITCH test suites | Deep project coverage | Not cross-stack by construction |

sipdrift is complementary: it consumes torture-style and operator-authored fixtures and asks a differential question — *do these stacks agree on these axes under this input?*

# Experiments (Host B lab, 5 Sep 2026)

Lab host: ephemeral Host B `10.4.0.32` (Ubuntu 24.04). Installed Sofia-SIP `1.12.11` from distro packages; built PJSIP (pjproject) from upstream source. Expanded corpus to **32** fixtures. Experiment classes:

1. **Driver-pair suites** — full corpus across all registered driver pairs (`builtin`, `pjsip-stub`, `sofia-stub`, `sofia-lab`, `pjsip-lab`).
2. **Per-fixture spotlight** — `builtin` vs lab drivers on every fixture ID.
3. **Sofia CLI tool smokes** — `sip-date`, `localinfo`, `addrinfo`, `sip-dig`, `sip-options`, `stunc`.
4. **Live OPTIONS** — UDP responder + `sip-options` against `127.0.0.1`.
5. **pytest regression** — package test suite on the lab venv.

Packs are archived under lab pull notes; stub-tier pairs agree on shared parse axes, while lab-vs-reference pairs surface honest normalization differences (compact-form expansion, whitespace, phrase formatting) that populate `docs/DIVERGENCES.md`.

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

Expected: `compare` exit **0** (`agree`); `suite` exit **1** when the malformed fixture errors (remaining cases agree under stub pairs).

JSON:

```bash
python -m sipdrift.cli compare F-200-MIN --format json
python -m sipdrift.cli drivers
python -m sipdrift.cli fixtures
```

## Lab path (optional)

On a host with Sofia-SIP development packages:

```bash
cd tools && make sofia
export SIPDRIFT_SOFIA_OBSERVE=$PWD/sofia_observe
python -m sipdrift.cli suite --left builtin --right sofia-lab
```

With a built pjproject tree:

```bash
cd tools && make pjsip PJDIR=/path/to/pjproject
export SIPDRIFT_PJSIP_OBSERVE=$PWD/pjsip_observe
python -m sipdrift.cli suite --left builtin --right pjsip-lab
```

## Continuous integration

GitHub Actions (`.github/workflows/ci.yml`) runs `pytest` on pushes and pull requests to `main`.

# Acknowledgements

Thanks to maintainers of PJSIP and Sofia-SIP for open libraries that make lab drivers possible, and to operators who share SIP edge-case traces that inform fixture design.

## AI usage disclosure

Drafting and refactoring of harness code and this manuscript were assisted by AI coding tools under author direction. All experimental claims, fixture contents, oracle definitions, and final wording were reviewed and accepted by the author. No AI system is listed as an author or contributor.

# References
