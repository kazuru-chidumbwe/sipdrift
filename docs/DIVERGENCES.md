# Known divergences (stub tier)

Honest record of cross-stack divergences observed under pinned fixtures.

**Last updated:** 2026-08-30 · **Harness version:** 0.2.0 · **Oracle axes:** `start_line`, `status_code`, `via`, `cseq`

## Stub-tier runs (parse-path only)

| Fixture pair | Left | Right | Status | Notes |
| --- | --- | --- | --- | --- |
| All corpus × default | `builtin` | `pjsip-stub` | **agree** | Parse-path stubs share identical axes |
| All corpus × OSS pair | `pjsip-stub` | `sofia-stub` | **agree** | Parse-path stubs share identical axes |
| `F-MALFORMED-START` | any | any | **error** | Empty fixture — both drivers fail parse |

**No semantic divergences** are claimed at stub tier. Real divergences require lab subprocess drivers (PJSIP, Sofia-SIP) — see [`LAB-PJSIP.md`](LAB-PJSIP.md).

## Lab tier (pending)

| Fixture | Stacks | Status | Notes |
| --- | --- | --- | --- |
| — | — | — | Populate after Lab Test Server driver runs |

## Taxonomy

| Status | Meaning |
| --- | --- |
| agree | All oracle axes match |
| diverge | One or more axes differ |
| error | One or both drivers failed |
| skip | Driver or axis unavailable |
