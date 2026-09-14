# sipdrift

Differential testing harness for open-source SIP/VoIP stacks.

Pinned SIP fixtures are observed through multiple drivers, normalized onto shared oracle axes (start-line, status, Via, CSeq, Content-Type/Length, body and SDP digests), and classified as `agree`, `diverge`, `error`, or `skip`.

## Status

**`0.3.3`** — 53 fixtures · seven drivers · Host B pack pins.

Headline comparisons are **lab versus lab** (real OSS stacks). `builtin` and `*-stub` drivers are for CI and calibration — not a fourth SIP stack.

| Headline pair | Role |
| --- | --- |
| `pjsip-lab` vs `sofia-lab` | UA library vs UA library |
| `pjsip-lab` / `sofia-lab` vs `kamailio-lab` | UA library vs proxy receive path |

Drivers: `builtin` · `pjsip-stub` · `sofia-stub` · `kamailio-stub` · `pjsip-lab` · `sofia-lab` · `kamailio-lab`

## Quick check (stub / CI)

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
sipdrift compare F-200-MIN
sipdrift suite --right sofia-stub
```

## Lab path (optional)

Requires host-built observe helpers — see [`docs/LAB-DRIVERS.md`](docs/LAB-DRIVERS.md).

```bash
make -C tools sofia
export SIPDRIFT_SOFIA_OBSERVE=$PWD/tools/sofia_observe
make -C tools pjsip PJDIR=/path/to/pjproject
export SIPDRIFT_PJSIP_OBSERVE=$PWD/tools/pjsip_observe
sipdrift suite --left pjsip-lab --right sofia-lab

bash tools/kamailio/start_observe.sh
export SIPDRIFT_KAMAILIO_PORT=5090
sipdrift suite --left sofia-lab --right kamailio-lab
sipdrift suite --left pjsip-lab --right kamailio-lab
```

Known divergences: [`docs/DIVERGENCES.md`](docs/DIVERGENCES.md) · Kamailio scope: [`docs/KAMAILIO-SCOPE.md`](docs/KAMAILIO-SCOPE.md).

Reproduce Host B-style suites with `tools/run_hostb_experiments.py` on a lab host that has observe binaries installed.

## Cite

See [`CITATION.cff`](CITATION.cff). Changelog: [`CHANGELOG.md`](CHANGELOG.md).

## Contributing and support

Contributions via issues and pull requests are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). Best-effort maintainer response; this is an independent research project.

## License

MIT — see [LICENSE](LICENSE).
