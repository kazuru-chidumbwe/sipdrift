# Contributing to sipdrift

Thanks for interest in improving the harness. sipdrift is maintained by a single author; contributions via GitHub issues and pull requests are welcome.

## Support

- **Issues:** use [GitHub Issues](https://github.com/kazuru-chidumbwe/sipdrift/issues) for bugs, fixture proposals, and driver ideas.
- **Pull requests:** open against `main`. Prefer small, focused changes.
- **Response expectation:** best-effort; this is an independent research project, not a commercial support channel.

## Development setup

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m sipdrift.cli compare F-200-MIN
```

Stub drivers (`builtin`, `*-stub`) run without native SIP libraries. Lab drivers (`pjsip-lab`, `sofia-lab`, `kamailio-lab`) need host-pinned observe binaries — see [`docs/LAB-DRIVERS.md`](docs/LAB-DRIVERS.md).

## What belongs where

| Change | Prefer |
| --- | --- |
| New fixture | `fixtures/*.sip` + short note in `fixtures/README.md` |
| Oracle / classification | `sipdrift/harness.py` + tests under `tests/` |
| Stub driver | `sipdrift/drivers/` + registry entry |
| Lab observe helper | `tools/` + docs update |
| Paper / JOSS pack | `paper/` |

## Commit style

- Prefer short imperative subjects (`Add …`, `Fix …`, `docs: …`).
- Do not add AI tooling or IDE products as co-authors or contributors in commits, README, CITATION, or the paper.
- Keep experimental claims tied to pinned packs or reproducible CLI commands.

## Scope boundaries

- Headline interop claims are **lab-vs-lab** (real OSS stacks). `builtin` is a reference parse path for calibration and CI — not a fourth SIP stack.
- Divergences are normalization-class findings under the oracle axes, not CVE claims.
- Do not invent Host B Results; re-run `tools/run_hostb_experiments.py` on a lab host and compare digests to `paper/paper.md`.
