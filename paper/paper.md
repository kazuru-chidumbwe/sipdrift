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

**sipdrift** is an open-source differential testing harness for SIP message handling. It runs a pinned corpus of SIP fixtures through multiple stack drivers, normalizes each driver's observations onto shared oracle axes (start-line, status code, Via, CSeq, Content-Type, Content-Length, body and SDP digests), and classifies each fixture as `agree`, `diverge`, `error`, or `skip`. The harness ships a Python package with a `StackDriver` protocol, stub and lab drivers for PJSIP, Sofia-SIP, and Kamailio, a `compare`/`suite` CLI with text and JSON reports, GitHub Actions continuous integration, and a JOSS-oriented paper pack under `paper/`.

# Statement of need

Production VoIP platforms assemble SIP proxies, media servers, session border controllers, and edge firewalls from different vendors and OSS projects. RFC 3261 conformance is necessary but not sufficient: stacks diverge on compact-form headers, folded header lines, whitespace tolerance, escaped URIs, unknown methods, incomplete messages, and how they treat message bodies and SDP [@rfc3261; @rfc4475]. Those divergences matter for operators who must reason about what a peer will accept or rewrite, and for researchers studying protocol robustness and defence-in-depth at the signalling layer.

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

From **0.3.3**, the default oracle compares:

| Axis | Meaning |
| --- | --- |
| `start_line` | First non-empty request or status line |
| `status_code` | Numeric response code when present |
| `via` | First Via header value |
| `cseq` | CSeq header value |
| `content_type` | Content-Type / compact `c` |
| `content_length` | Content-Length / compact `l` (integer) |
| `body_sha256` | SHA-256 of the raw body bytes |
| `sdp_sha256` | SHA-256 of normalized SDP when Content-Type is `application/sdp`; else null |

Outcomes: `agree` · `diverge` · `error` · `skip`. Body axes fingerprint the delivered fixture body (and a stable SDP normalization); they do not yet compare stack re-serialization of media descriptions.

## Driver tiers

| Driver | Tier | Backend |
| --- | --- | --- |
| `builtin` | Reference | Pure-Python parse path (not an OSS SIP stack) |
| `pjsip-stub` / `sofia-stub` | Stub | Same parse path; documents intended OSS targets |
| `pjsip-lab` | Lab | `tools/pjsip_observe` (`pjsip_parse_msg`) |
| `sofia-lab` | Lab | `tools/sofia_observe` (Sofia `msg_make`) |
| `kamailio-stub` / `kamailio-lab` | Stub / Lab | Proxy-tier UDP observe (`tools/kamailio/`) |

CI exercises stub and reference drivers so the package remains installable without native SIP libraries. Lab drivers are optional and host-pinned.

## Fixture corpus

Version **0.3.3** ships **53** fixtures: happy-path requests/responses, dialog methods, event packages, INVITE/200 with SDP bodies, compact Content-Type, plain MESSAGE bodies, compact/folded/multi-Via, case and whitespace edges, incomplete messages, and an expanded RFC 4475–inspired torture set (LWS, escaped/long URIs, mismatched and duplicate Content-Length, duplicate Via/CSeq, non-ASCII Warning, NUL-in-body, IPv6 Via, display-names, unknown URI schemes, Request-URI parameters, empty Subject, missing magic cookie).

## Threats to validity

- Drivers observe **parse/normalization** of a fixture blob — not full transaction or media state machines.
- Body/SDP digests are wire fingerprints (plus SDP whitespace normalization); stacks that rewrite SDP on the wire are out of scope until a re-serialize path exists.
- Normalization differences are real under the chosen axes, but may be intentional stack policy.
- Lab binaries are host-pinned; reproducers without Sofia/PJSIP/Kamailio fall back to stubs.
- `kamailio-lab` is a **proxy receive** path (UDP + script dump), not a production routing configuration [@kamailio].

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

Ephemeral Ubuntu 24.04 lab host (16 vCPU). Sofia-SIP `1.12.11` and Kamailio `5.7.4` from distro packages; PJSIP built from upstream pjproject. Packs under a host-local `/opt/atlas/sipdrift-packs/` tree. Canonical Results pack: **`sipdrift-hostb-20260905T015940Z`** (`0.3.3`, 53 fixtures, seven drivers including `kamailio-lab`).

## Experiment classes

1. Full-corpus **driver-pair suites** (all ordered pairs among seven drivers — **105** indexed experiments in the 0.3.3 pack).
2. Per-fixture spotlights (builtin vs sofia-lab).
3. Sofia CLI tool smokes.
4. **Live OPTIONS** (UDP responder + `sip-options`).
5. **pytest** on the lab virtualenv.
6. **Kamailio observe listener** (`tools/kamailio/`) — UDP fixture delivery → Lua JSON axes.

## Headline suite outcomes (0.3.3 pack, 53 fixtures)

| Pair | agree | diverge | error |
| --- | ---: | ---: | ---: |
| Stub pairs | 52 | 0 | 1 |
| `builtin` vs `sofia-lab` | 49 | 3 | 1 |
| `pjsip-lab` vs `sofia-lab` | 48 | 1 | 4 |
| `builtin` vs `kamailio-lab` | 41 | 6 | 6 |
| `sofia-lab` vs `kamailio-lab` | 41 | 6 | 6 |
| `pjsip-lab` vs `kamailio-lab` | 41 | 5 | 7 |

Kamailio errors concentrate on incomplete messages and some required-header absences — expected for a proxy receive path. New torture cases (`F-TORTURE-MULTI-CLEN`, `F-TORTURE-UNKNOWN-SCHEME`, trailing Via whitespace) add diverge/error rows without changing the headline class of findings. SDP body fixtures agree across stub and lab pairs under the wire-body axes. Divergences remain normalization-class, not claimed as CVEs.

## Notable divergences

| Fixture | Pair | Axis behaviour |
| --- | --- | --- |
| `F-FOLDED-VIA` | builtin vs sofia/kamailio-lab | Fold unfold / retained continuation whitespace |
| `F-LOWER-SIP` | cross-lab | Method / SIP-version case policy differs |
| `F-SPACES-START` | builtin vs sofia-lab | Sofia collapses status whitespace; Kamailio often **errors** |
| `F-TORTURE-WS-END` · `F-TORTURE-DUP-VIA` · `F-TORTURE-MULTI-CLEN` | vs kamailio-lab | Via extraction / receive-path oddities |
| `F-TORTURE-UNKNOWN-SCHEME` | vs kamailio / pjsip-lab | Unknown Request-URI scheme → empty R-URI or parse error |

## Live OPTIONS

Responder `0.0.0.0:15060`; `sip-options -m sip:127.0.0.1:15061 sip:127.0.0.1:15060` — default / `--all` / `--1XX` all **rc=0**.


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

bash tools/kamailio/start_observe.sh
export SIPDRIFT_KAMAILIO_PORT=5090
python -m sipdrift.cli suite --left sofia-lab --right kamailio-lab
python tools/run_hostb_experiments.py
```

## Continuous integration

GitHub Actions (`.github/workflows/ci.yml`) runs `pytest` on pushes and pull requests to `main`.

# Acknowledgements

Thanks to maintainers of PJSIP, Sofia-SIP, and Kamailio for open SIP software that makes lab drivers possible, and to operators who share edge-case traces that inform fixture design.

## AI usage disclosure

Drafting and refactoring of harness code and this manuscript were assisted by AI coding tools under author direction. All experimental claims, fixture contents, oracle definitions, and final wording were reviewed and accepted by the author. No AI system is listed as an author or contributor.

# References
