# sipdrift

Differential testing harness for open-source SIP/VoIP stacks.

## Status

**`0.3.2`** — PJSIP + Sofia **library** labs, **Kamailio proxy-tier** lab (`kamailio-lab`), 40 fixtures, JOSS draft under `paper/`.

Drivers: `builtin` · `pjsip-stub` · `sofia-stub` · `kamailio-stub` · `pjsip-lab` · `sofia-lab` · `kamailio-lab`

## Quick check

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
sipdrift compare F-200-MIN
sipdrift suite --right sofia-stub
```

## Kamailio lab (optional)

```bash
bash tools/kamailio/start_observe.sh
export SIPDRIFT_KAMAILIO_PORT=5090
sipdrift suite --left builtin --right kamailio-lab
```

See [`docs/KAMAILIO-SCOPE.md`](docs/KAMAILIO-SCOPE.md) · [`docs/DIVERGENCES.md`](docs/DIVERGENCES.md) · [`docs/LAB-DRIVERS.md`](docs/LAB-DRIVERS.md).

## License

MIT — see [LICENSE](LICENSE).
