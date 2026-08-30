# PJSIP lab driver (Phase 2 — planned)

Real PJSIP integration runs on **Lab Test Server** (`LAB_HOST2` / Tailscale `100.110.54.48`), not local Docker Desktop.

## Target

- Build or install `pjsua` / pjproject on `/opt/atlas`
- Driver `pjsip-lab` invokes subprocess with fixture on stdin or SIP file path
- Normalize output to `StackObservation` axes

## Environment (planned)

| Variable | Purpose |
| --- | --- |
| `SIPDRIFT_PJSUA_BIN` | Path to `pjsua` binary on lab host |
| `SIPDRIFT_LAB_HOST` | SSH target (default from Atlas lab pin) |

## Current state

`pjsip-stub` uses parse-path only. Do not claim lab results until this driver ships.

## References

- PJSIP: https://www.pjsip.org/ (GPL-2.0)
- Atlas lab pin: `CURRENT-WORK/notes/lab/PERMANENT-LAB-PIN-2026-08-10.md`
