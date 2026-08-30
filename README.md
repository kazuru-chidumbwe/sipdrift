# Sipdrift

A differential testing harness for open-source SIP/VoIP stacks.

## Status

**Early development (`0.2.0`).** Multi-axis oracle + OSS stub pair; lab drivers pending.

Current layout:

- installable package (`sipdrift`)
- CLI: `status` · `fixtures` · `drivers` · `compare` · `suite` · `--version`
- parse axes: start-line · status code · Via · CSeq
- fixture corpus (`fixtures/` — 7 pinned cases)
- stack drivers: `builtin` · `pjsip-stub` · `sofia-stub`
- compare harness with multi-axis oracle
- pytest suite + GitHub Actions CI

## Quick check

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
sipdrift compare F-200-MIN
sipdrift suite --right sofia-stub
```

## Compare

```bash
sipdrift compare F-200-MIN
sipdrift compare F-200-MIN --left pjsip-stub --right sofia-stub
sipdrift compare F-200-MIN --format json
```

## Suite

```bash
sipdrift suite
sipdrift suite --left builtin --right sofia-stub --format json
```

Exit codes: `0` agree / all agree · `1` diverge/error · `2` skip/usage error.

## Drivers

| Name | Type | Notes |
| --- | --- | --- |
| `builtin` | Internal reference | Parse-path axes |
| `pjsip-stub` | PJSIP-target (GPL-2.0) | Parse-path; lab hook in `docs/LAB-PJSIP.md` |
| `sofia-stub` | Sofia-SIP-target (LGPL-2.1) | Parse-path stub |

## Oracle axes

`start_line` · `status_code` · `via` · `cseq`

Known results: [`docs/DIVERGENCES.md`](docs/DIVERGENCES.md)

## License

MIT — see [LICENSE](LICENSE).

PJSIP (GPL-2.0) and Sofia-SIP (LGPL-2.1) are planned lab stacks.
