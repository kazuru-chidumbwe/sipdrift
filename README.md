# Sipdrift

A testing framework for open-source SIP/VoIP stacks.

## Status

**Early scaffold (`0.0.2`).** Not ready for use.

Weekend-2 (2026-08-08):

- installable package stub (`sipdrift`)
- CLI: `sipdrift status` · `sipdrift fixtures` · `--version`
- start-line stub (`sipdrift.parse`)
- fixture corpus stub (`fixtures/` · `F-INVITE-MIN` · `F-200-MIN`)
- compare-harness outline (`sipdrift.harness.classify_start_lines`) — **no stack drivers yet**
- smoke tests under `tests/`

See [`docs/WEEKEND-LOG.md`](docs/WEEKEND-LOG.md) for the JOSS age-clock cadence.

## Quick check

```bash
python -m pip install -e ".[dev]"
sipdrift --version
sipdrift fixtures
pytest
```

## License

MIT — see [LICENSE](LICENSE).
