# Sipdrift

A testing framework for open-source SIP/VoIP stacks.

## Status

**Early scaffold (`0.0.1`).** Not ready for use.

Weekend-2 layout (2026-08-08):

- installable package stub (`sipdrift`)
- CLI: `sipdrift status` / `--version`
- start-line stub only (`sipdrift.parse.split_start_line`)
- smoke tests under `tests/`

See [`docs/WEEKEND-LOG.md`](docs/WEEKEND-LOG.md) for the JOSS age-clock cadence.

## Quick check

```bash
python -m pip install -e ".[dev]"
sipdrift --version
pytest
```

## License

MIT — see [LICENSE](LICENSE).
