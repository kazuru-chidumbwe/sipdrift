# Lab drivers (PJSIP + Sofia-SIP)

Real stack parsers run on a Linux lab host (Atlas Host B / Lab Test Server), **not** local Docker Desktop on the Windows workstation.

## Sofia-SIP (`sofia-lab`)

```bash
sudo apt-get install -y sofia-sip-bin libsofia-sip-ua-dev build-essential pkg-config
cd tools && make sofia
export SIPDRIFT_SOFIA_OBSERVE=$PWD/sofia_observe
python -m sipdrift.cli suite --left builtin --right sofia-lab
```

Helper: `tools/sofia_observe.c` → uses Sofia `msg_make` / `sip_object`.

## PJSIP (`pjsip-lab`)

Build [pjproject](https://github.com/pjsip/pjproject), then:

```bash
cd tools
make pjsip PJDIR=/path/to/pjproject
export SIPDRIFT_PJSIP_OBSERVE=$PWD/pjsip_observe
python -m sipdrift.cli suite --left builtin --right pjsip-lab
```

Helper: `tools/pjsip_observe.c` → uses `pjsip_parse_msg`.

## Kamailio (`kamailio-lab`)

```bash
sudo apt-get install -y kamailio kamailio-lua-modules
bash tools/kamailio/start_observe.sh
export SIPDRIFT_KAMAILIO_HOST=127.0.0.1
export SIPDRIFT_KAMAILIO_PORT=5090
export SIPDRIFT_KAMAILIO_OBS=/tmp/sipdrift-kamailio-obs.json
python -m sipdrift.cli suite --left sofia-lab --right kamailio-lab
```

See [`KAMAILIO-SCOPE.md`](KAMAILIO-SCOPE.md).

| Variable | Purpose |
| --- | --- |
| `SIPDRIFT_SOFIA_OBSERVE` | Path to `sofia_observe` binary |
| `SIPDRIFT_PJSIP_OBSERVE` | Path to `pjsip_observe` binary |

Without these binaries, lab drivers report `ok=false` (ERROR in compares). Stub drivers remain the CI path.

## Experiment runner

`tools/run_hostb_experiments.py` sweeps all driver pairs, per-fixture spotlights, Sofia CLI tools, optional live OPTIONS, and pytest. Writes a pack under `/opt/atlas/sipdrift-packs/`.

## References

- PJSIP: https://www.pjsip.org/ (GPL-2.0)
- Sofia-SIP: https://github.com/freeswitch/sofia-sip (LGPL-2.1)
