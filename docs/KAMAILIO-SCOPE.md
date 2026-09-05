# Kamailio scope (planned stack #3)

**Status:** scope note only — no lab driver in `0.3.x`.

| Field | Value |
| --- | --- |
| Project | [Kamailio](https://www.kamailio.org/) |
| Licence | GPL |
| Role | SIP proxy / registrar / edge — not a UA library |
| Why later | Proxy observation needs transaction or script-level hooks; heavier than fixture-in → parse-out |

## Honest claim boundary

sipdrift `0.3.x` differential claims cover **message parse/normalization** for PJSIP and Sofia-SIP lab drivers. Kamailio would add a **proxy-tier** observation path (e.g. `kamcmd` / module dump / scripted `xlog` of normalized fields) — out of scope until UA-pair lab results are stable in the JOSS narrative.

## When to open

After JOSS age clock is near and UA-pair Results tables are frozen — or if a sponsor asks for proxy-tier coverage earlier.
