# sipdrift

Differential testing harness for open-source SIP/VoIP stacks.

## Status

**`0.3.0`** — multi-axis oracle, expanded fixture corpus (32), stub drivers, and lab drivers for **PJSIP** (`pjsip-lab`) and **Sofia-SIP** (`sofia-lab`) via native observe helpers.

- installable package (`sipdrift`)
- CLI: `status` · `fixtures` · `drivers` · `compare` · `suite` · `--version`
- oracle axes: start-line · status code · Via · CSeq
- fixture corpus under `fixtures/`
- drivers: `builtin` · `pjsip-stub` · `sofia-stub` · `pjsip-lab` · `sofia-lab`
- pytest + GitHub Actions CI
- JOSS draft: `paper/paper.md` (submit gated by 6-month age clock ~Feb 2027+)

## Quick check (stub / CI path)

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
sipdrift compare F-200-MIN
sipdrift suite --right sofia-stub
```

## Lab drivers (optional)

Build observe helpers where Sofia-SIP and/or PJSIP are installed:

```bash
cd tools
make sofia
# optional: make pjsip PJDIR=/path/to/pjproject
export SIPDRIFT_SOFIA_OBSERVE=$PWD/sofia_observe
export SIPDRIFT_PJSIP_OBSERVE=$PWD/pjsip_observe   # if built
sipdrift suite --left builtin --right sofia-lab
sipdrift suite --left pjsip-lab --right sofia-lab
```

See [`docs/LAB-DRIVERS.md`](docs/LAB-DRIVERS.md).

## Compare / suite

```bash
sipdrift compare F-200-MIN --format json
sipdrift suite --left builtin --right sofia-stub --format json
sipdrift drivers
sipdrift fixtures
```

Exit codes: `0` agree / all agree · `1` diverge/error · `2` skip/usage error.

## Drivers

| Name | Type | Notes |
| --- | --- | --- |
| `builtin` | Reference | Pure-Python parse path |
| `pjsip-stub` | Stub | PJSIP-target (GPL-2.0) |
| `sofia-stub` | Stub | Sofia-SIP-target (LGPL-2.1) |
| `pjsip-lab` | Lab | `tools/pjsip_observe` (needs pjproject) |
| `sofia-lab` | Lab | `tools/sofia_observe` (needs libsofia-sip-ua) |

Known divergences: [`docs/DIVERGENCES.md`](docs/DIVERGENCES.md)

## License

MIT — see [LICENSE](LICENSE).

PJSIP (GPL-2.0) and Sofia-SIP (LGPL-2.1) remain separate lab dependencies.
