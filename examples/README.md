# Minimal walkthroughs for reviewers (stub / CI path).

## 1. Install and smoke

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m sipdrift.cli compare F-200-MIN
python -m sipdrift.cli suite --right sofia-stub
```

## 2. JSON report

```bash
python -m sipdrift.cli compare F-COMPACT-VIA --left builtin --right sofia-stub --format json
```

## 3. Lab path (optional)

Requires `tools/sofia_observe` and/or `tools/pjsip_observe` — see `docs/LAB-DRIVERS.md`.

```bash
export SIPDRIFT_SOFIA_OBSERVE=$PWD/tools/sofia_observe
python -m sipdrift.cli suite --left builtin --right sofia-lab --format json
```

## 4. Expected JSON (reviewer gold)

Checked-in samples under `examples/expected/` (includes body/SDP axes from **0.3.3**):

```bash
python -m sipdrift.cli compare F-200-MIN --left builtin --right sofia-stub --format json
# compare to examples/expected/F-200-MIN.builtin-vs-sofia-stub.json

python -m sipdrift.cli compare F-INVITE-SDP --left builtin --right sofia-stub --format json
# compare to examples/expected/F-INVITE-SDP.builtin-vs-sofia-stub.json
```

```bash
python tools/run_hostb_experiments.py
```

Writes `/opt/atlas/sipdrift-packs/sipdrift-hostb-<UTC>/`.
