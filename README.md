# Sipdrift

A differential testing harness for open-source SIP/VoIP stacks.

## Status

**Early development (`0.1.0`).** Compare loop works with stub drivers; not production-ready.

Current layout:

- installable package (`sipdrift`)
- CLI: `sipdrift status` · `sipdrift fixtures` · `sipdrift compare` · `--version`
- start-line parser (`sipdrift.parse`)
- fixture corpus (`fixtures/` — 7 pinned cases)
- stack drivers: `builtin` (reference) · `pjsip-stub` (PJSIP-target stub)
- compare harness (`sipdrift.run` + `classify_start_lines`)
- pytest suite + GitHub Actions CI

## Quick check

```bash
python -m pip install -e ".[dev]"
sipdrift --version
sipdrift fixtures
sipdrift compare F-200-MIN
pytest
```

## Compare

```bash
# Default: builtin vs pjsip-stub
sipdrift compare F-200-MIN

# JSON report
sipdrift compare F-200-MIN --format json

# Custom driver pair
sipdrift compare F-486-MIN --left builtin --right pjsip-stub
```

Exit codes: `0` agree · `1` diverge/error · `2` skip/usage error.

## Drivers

| Name | Type | Notes |
| --- | --- | --- |
| `builtin` | Internal reference | Start-line parse only |
| `pjsip-stub` | PJSIP-target stub | Parse-path; lab subprocess in Phase 2 |

## Fixtures

| ID | Intent |
| --- | --- |
| `F-INVITE-MIN` | Minimal INVITE |
| `F-200-MIN` | 200 OK response (smoke gate) |
| `F-486-MIN` | 486 Busy Here |
| `F-503-MIN` | 503 Service Unavailable |
| `F-OPTIONS-MIN` | OPTIONS request |
| `F-REGISTER-MIN` | REGISTER request |
| `F-MALFORMED-START` | Empty message (ERROR path) |

## License

MIT — see [LICENSE](LICENSE).

PJSIP (planned stack #1) is GPL-2.0 — see project docs when lab driver lands.
