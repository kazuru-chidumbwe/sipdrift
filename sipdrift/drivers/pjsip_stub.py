"""PJSIP-target stack driver stub.

PJSIP (https://www.pjsip.org/) is GPL-2.0. Phase 2 still uses parse-path;
lab subprocess hook documented in docs/LAB-PJSIP.md.
"""

from __future__ import annotations

from sipdrift.drivers.common import observe_from_parse


class PjsipStubDriver:
    """OSS-target stub for PJSIP — parse-path until lab subprocess lands."""

    @property
    def stack_id(self) -> str:
        return "pjsip-stub"

    def observe(self, raw: str):
        return observe_from_parse(self.stack_id, raw, detail="stub: parse-path only")
