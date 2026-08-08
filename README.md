# Sipdrift

A testing framework for open-source SIP/VoIP stacks.

## Status

**Early scaffold (`0.0.2`).** Not ready for use.

Current layout:

- installable package stub (`sipdrift`)
- CLI: `sipdrift status` · `sipdrift fixtures` · `--version`
- start-line stub (`sipdrift.parse`)
- fixture corpus stub (`fixtures/` · `F-INVITE-MIN` · `F-200-MIN`)
- compare-harness outline (`sipdrift.harness.classify_start_lines`) — **no stack drivers yet**
- smoke tests under `tests/`

## Quick check

```bash
python -m pip install -e ".[dev]"
sipdrift --version
sipdrift fixtures
pytest
```

## License

MIT — see [LICENSE](LICENSE).
