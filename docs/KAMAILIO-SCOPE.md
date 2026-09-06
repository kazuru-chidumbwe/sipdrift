# Kamailio lab driver (proxy tier)

**Status (0.3.3):** `kamailio-stub` + **`kamailio-lab`** shipped (unchanged; body axes filled from wire when Lua omits digests).

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

## Error fixtures (pack `…015940Z`)

Six fixtures against `kamailio-lab` return **error** in the `builtin` vs `kamailio-lab` suite (no observation JSON written). This is expected for the receive-only script path — not a harness bug.

| Fixture | Why Kamailio errors | Library labs |
| --- | --- | --- |
| `F-MALFORMED-START` | Unparseable start line; message dropped before Lua dump | builtin also errors |
| `F-SPACES-START` | Extra whitespace in status line; receive path rejects | Sofia may diverge instead |
| `F-NO-HEADERS` | Status line only; no headers for script to read | builtin still parses start line |
| `F-ONLY-START` | Request start line without required headers | Sofia/PJSIP may still parse |
| `F-MISSING-VIA` | Request without Via; proxy script does not emit axes | UA parsers often tolerate |
| `F-MISSING-CSEQ` | Request without CSeq; same | UA parsers often tolerate |

When `kamailio-lab` errors, the driver reports `no observation file from kamailio at /tmp/sipdrift-kamailio-obs.json`. Treat these rows as **proxy-tier receive limits**, not CVE claims.

## Pack

Canonical lab pack: **`sipdrift-hostb-20260905T015940Z`** (`0.3.3`, 53 fixtures) — see `docs/DIVERGENCES.md`.
