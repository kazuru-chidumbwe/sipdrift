# Kamailio lab driver (proxy tier)

**Status (0.3.2):** `kamailio-stub` + **`kamailio-lab`** shipped.

| Field | Value |
| --- | --- |
| Project | [Kamailio](https://www.kamailio.org/) 5.7.x |
| Licence | GPL |
| Role | SIP proxy observe listener (UDP) — not a full routing proxy |
| Lab path | `tools/kamailio/` cfg + Lua dump → JSON axes |

## Honest claim boundary

`kamailio-lab` observes **what Kamailio’s script sees** when a fixture is delivered as a UDP SIP message to `127.0.0.1:5090`. Request fixtures hit `request_route`; incomplete/stray messages may **error**. This is a **proxy-tier receive parse** path, complementary to PJSIP/Sofia library parse helpers.

## Host B quick start

```bash
sudo apt-get install -y kamailio kamailio-lua-modules
bash tools/kamailio/start_observe.sh
export SIPDRIFT_KAMAILIO_HOST=127.0.0.1 SIPDRIFT_KAMAILIO_PORT=5090
export SIPDRIFT_KAMAILIO_OBS=/tmp/sipdrift-kamailio-obs.json
python -m sipdrift.cli suite --left sofia-lab --right kamailio-lab
```

## Pack

`sipdrift-hostb-20260905T012956Z` — see `docs/DIVERGENCES.md`.
