# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Headline docs lead with lab-vs-lab pairs; `builtin` framed as calibration.
- Removed venue-oriented draft pack from the public tree; product docs only.

## [0.3.3] — 2026-09-05

### Added

- Body and SDP oracle axes (`body_sha256`, `sdp_sha256`, Content-Type / Content-Length).
- Expanded RFC 4475–class torture corpus — **53** fixtures total.
- Canonical Host B pack `sipdrift-hostb-20260905T015940Z` digests recorded in divergences docs.

### Changed

- Divergences and Results framing for the 0.3.3 pack.

## [0.3.2] — 2026-09-05

### Added

- `kamailio-stub` and `kamailio-lab` (UDP + Lua observe).
- Seven-driver Host B pack `…012956Z` and expected JSON examples.

## [0.3.1] — 2026-09-05

### Added

- Torture fixture expansion (40 fixtures).
- Live OPTIONS lab path repair.
- Examples walkthrough under `examples/`.

## [0.3.0] — 2026-09-05

### Added

- `pjsip-lab` and `sofia-lab` observe helpers.
- 32-fixture corpus and Host B experiment pack.

## [0.2.0] — 2026-08-30

### Added

- Multi-axis oracle (`start_line`, `status_code`, `via`, `cseq`).
- `sofia-stub` driver.
- `sipdrift suite` command and divergences documentation.

## [0.1.0] — 2026-08-30

### Added

- `StackDriver` protocol, `builtin` and `pjsip-stub`.
- `sipdrift compare` CLI and expanded fixture corpus.
- GitHub Actions pytest CI.
- Smoke gate: `compare F-200-MIN` → agree.

## [0.0.2] — 2026-08-08

### Added

- Fixture corpus samples and compare-harness outline.
- `fixtures` CLI surface.

## [0.0.1] — 2026-08-08

### Added

- Installable package scaffold, CLI stub, start-line parse placeholder, smoke tests.
