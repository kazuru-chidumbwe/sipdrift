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
date: 13 September 2026
bibliography: paper.bib
---

# Summary

Session Initiation Protocol (SIP) stacks are the control-plane substrate for Voice over IP (VoIP), unified communications, and many telecom edge deployments [@rfc3261]. Open-source implementations — notably PJSIP [@pjsip], Sofia-SIP [@sofia], and Kamailio-class proxies [@kamailio] — are routinely combined in production platforms and research testbeds. Interoperability defects and semantic divergences between stacks are a recurring source of mis-routing, toll-fraud exposure, and security bypasses that single-stack conformance suites do not surface.

**sipdrift** is an open-source differential testing harness for SIP message handling. It runs a pinned corpus of SIP fixtures through multiple stack drivers, normalizes each driver's observations onto shared oracle axes (start-line, status code, Via, CSeq, Content-Type, Content-Length, body and SDP digests), and classifies each fixture as `agree`, `diverge`, `error`, or `skip`. The package ships a `StackDriver` protocol, stub and lab drivers for PJSIP, Sofia-SIP, and Kamailio, a `compare`/`suite` CLI with text and JSON reports, continuous integration, and this JOSS paper pack under `paper/`.

# Statement of need

Production VoIP platforms assemble SIP proxies, media servers, session border controllers, and edge firewalls from different vendors and OSS projects. RFC 3261 conformance is necessary but not sufficient: stacks diverge on compact-form headers, folded lines, whitespace, escaped URIs, unknown methods, incomplete messages, and body/SDP handling [@rfc3261; @rfc4475]. Those divergences matter for operators comparing upgrades and for researchers studying signalling robustness.

Existing SIP tooling clusters into four incomplete categories: load tools such as SIPp [@sipp]; live interop events such as SIPit [@sipit]; single-stack unit and conformance tests; and fuzzers that rarely emit structured cross-stack agreement classifications [@afl; @resolfuzz; @resolverfuzz].

sipdrift supplies a **repeatable differential oracle**: identical fixtures, multiple drivers, shared axes, and machine-readable outcomes. Who benefits: operators under controlled cut-over inputs; security researchers documenting parser drift; OSS maintainers adding regression fixtures when a divergence is fixed or accepted as intentional.

# State of the field

| Approach | Strength | Gap vs sipdrift |
| --- | --- | --- |
| SIPp scenarios [@sipp] | Scalable load, scripted call flows | Single-target; no multi-stack normalized oracle |
| SIPit / interop events [@sipit] | Live multi-vendor exposure | Not a pinned, replayable corpus |
| RFC 4475 torture tests [@rfc4475] | Canonical hard cases | Usually applied one stack at a time |
| Differential DNS fuzzing [@resolfuzz; @resolverfuzz] | Semantic diverge discovery | DNS, not SIP message fixtures |
| Project-local test suites | Deep coverage for one stack | Not cross-stack by construction |

sipdrift asks: *do these stacks agree on these axes under this input?* Headline answers come from **lab-vs-lab** pairs. The `builtin` driver is a harness reference parser for calibration, not a stack in the interop claim.

# Software design

```text
fixture (.sip) → StackDriver.observe() × N → classify_observations() → report
```

| Layer | Module | Role |
| --- | --- | --- |
| Fixtures | `fixtures/*.sip` | Pinned SIP inputs (CRLF wire; stable IDs) |
| Drivers | `sipdrift.drivers` | `StackDriver` implementations per tier |
| Harness | `sipdrift.harness` | Multi-axis classification oracle |
| CLI | `sipdrift.cli` | `status`, `fixtures`, `drivers`, `compare`, `suite` |
| Lab tools | `tools/*_observe`, `tools/kamailio/` | Subprocess / UDP adapters |

Default oracle axes (from **0.3.3**): `start_line`, `status_code`, `via`, `cseq`, `content_type`, `content_length`, `body_sha256`, `sdp_sha256`. Outcomes: `agree` · `diverge` · `error` · `skip`. Body axes fingerprint wire bytes (plus SDP whitespace normalization); they do not yet compare stack re-serialization of media descriptions.

| Driver | Tier | Backend |
| --- | --- | --- |
| `builtin` | Reference | Pure-Python parse path (not an OSS SIP stack) |
| `*-stub` | Stub | Same parse path; documents OSS targets |
| `pjsip-lab` / `sofia-lab` | Lab | Native observe helpers |
| `kamailio-lab` | Lab | Proxy-tier UDP observe |

CI exercises stub and reference drivers without native SIP libraries. Lab drivers are optional and host-pinned. Version **0.3.3** ships **53** fixtures spanning happy-path, compact/folded headers, SDP bodies, and an RFC 4475–inspired torture set.

Threats to validity: observation covers parse/normalization of fixture blobs, not full transaction or media state machines; lab binaries are host-pinned; `kamailio-lab` is a proxy receive path, not a production routing configuration [@kamailio]; agreement among `builtin`/`*-stub` is not evidence that OSS stacks agree.

# Research impact statement

sipdrift is used in the author's own research workflow to measure cross-stack SIP parse/normalization agreement under a pinned corpus. The Host B laboratory pack **`sipdrift-hostb-20260905T015940Z`** (`0.3.3`) records suite outcomes and SHA-256 pins that this paper cites; those runs are developer research use of the software, not a separate measurement claim for JOSS. The intended research applications are (1) controlled comparison of candidate SIP stacks before cut-over and (2) documenting normalization drift that informs robustness and defence-in-depth hypotheses at the signalling layer. External adoption beyond the author is not claimed at submission time.

# Example evaluation

Ephemeral Ubuntu 24.04 lab host; Sofia-SIP `1.12.11` and Kamailio `5.7.4` from distro packages; PJSIP from upstream pjproject. Pack index SHA-256:

```
7231d56540708c3406c2f0b3af4b53f9f61ce9d304ac1c01a1f9c219f7bd126a
```

Headline **lab versus lab** suite outcomes (53 fixtures):

| Pair | agree | diverge | error |
| --- | ---: | ---: | ---: |
| `pjsip-lab` vs `sofia-lab` | 48 | 1 | 4 |
| `pjsip-lab` vs `kamailio-lab` | 41 | 5 | 7 |
| `sofia-lab` vs `kamailio-lab` | 41 | 6 | 6 |

Secondary `builtin` / stub rows are calibration only (see `docs/DIVERGENCES.md`). Against `kamailio-lab`, six fixtures error because the UDP receive script never writes an observation (`F-MALFORMED-START`, `F-SPACES-START`, `F-NO-HEADERS`, `F-ONLY-START`, `F-MISSING-VIA`, `F-MISSING-CSEQ`) — expected for a proxy path that drops incomplete messages before the Lua dump. Notable lab-vs-lab divergences include method/version case (`F-LOWER-SIP`), folded Via whitespace (`F-FOLDED-VIA`), and unknown Request-URI schemes. All reported divergences are normalization-class findings — not CVE claims. A live OPTIONS UDP round-trip on the same host exits **0** outside the fixture replay path.

# Reproducibility

```bash
git clone https://github.com/kazuru-chidumbwe/sipdrift.git
cd sipdrift
python -m pip install -e ".[dev]"
python -m pytest -q
python -m sipdrift.cli compare F-200-MIN
python -m sipdrift.cli suite --right sofia-stub
```

Lab path (optional): build observe helpers, then `suite --left pjsip-lab --right sofia-lab` and Kamailio lab pairs as in `examples/README.md`. GitHub Actions runs `pytest` on `main`. Canonical pack **`sipdrift-hostb-20260905T015940Z`**:

| Object | SHA-256 |
| --- | --- |
| `EXPERIMENT-INDEX.json` | `7231d56540708c3406c2f0b3af4b53f9f61ce9d304ac1c01a1f9c219f7bd126a` |
| Pack checksum-list (5 files) | `9dcb47784c11db42b4e83778fe9244b6445cd200a1b479bbbd93952edc66a3e3` |
| `E-suite-pjsip-lab-vs-sofia-lab.json` | `04a057e9ff7b315c293b30add63dbdc8891b62bad1252cbb87863a809a017cf8` |
| `E-suite-sofia-lab-vs-kamailio-lab.json` | `854a74ee52a3667428be662199c3018de8b1e282ab8fe44e225d3bf167efec0e` |

Reproduce with `tools/run_hostb_experiments.py` on a lab host that has Sofia/PJSIP/Kamailio observe binaries.

# Acknowledgements

Thanks to maintainers of PJSIP, Sofia-SIP, and Kamailio for open SIP software that makes lab drivers possible, and to operators who share edge-case traces that inform fixture design.

# AI usage disclosure

Generative AI coding assistants were used under author direction for drafting and refactoring harness code, documentation, and this manuscript. The author made the architectural and oracle design decisions, authored and curated the fixture corpus, ran and pinned laboratory experiments, and reviewed, edited, and validated all AI-assisted outputs before publication. No AI system is listed as an author or contributor.

# References
