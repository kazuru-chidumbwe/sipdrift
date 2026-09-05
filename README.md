# sipdrift

Differential testing harness for open-source SIP/VoIP stacks.

## Status

**`0.3.1`** — multi-axis oracle, **40** fixtures (incl. RFC 4475–inspired torture), stub + lab drivers (`pjsip-lab`, `sofia-lab`), live OPTIONS experiment path, JOSS draft under `paper/`.

- CLI: `status` · `fixtures` · `drivers` · `compare` · `suite`
- oracle axes: start-line · status code · Via · CSeq
- pytest + GitHub Actions CI
- examples: `examples/README.md`
- Kamailio scope note: `docs/KAMAILIO-SCOPE.md` (not implemented)

## Quick check (stub / CI path)

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
sipdrift compare F-200-MIN
sipdrift suite --right sofia-stub
```

## Lab drivers (optional)

```bash
cd tools && make sofia
export SIPDRIFT_SOFIA_OBSERVE=$PWD/sofia_observe
sipdrift suite --left builtin --right sofia-lab
```

See [`docs/LAB-DRIVERS.md`](docs/LAB-DRIVERS.md). Divergences: [`docs/DIVERGENCES.md`](docs/DIVERGENCES.md).

## License

MIT — see [LICENSE](LICENSE).
