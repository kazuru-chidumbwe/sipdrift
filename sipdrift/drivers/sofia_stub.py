"""Sofia-SIP-target stack driver stub.

Sofia-SIP (https://github.com/freeswitch/sofia-sip) is LGPL-2.1. Used in
FreeSWITCH-class stacks. Phase 2 parse-path stub; real driver follows lab work.
"""

from __future__ import annotations

from sipdrift.drivers.common import observe_from_parse


class SofiaStubDriver:
    """OSS-target stub for Sofia-SIP — parse-path until lab subprocess lands."""

    @property
    def stack_id(self) -> str:
        return "sofia-stub"

    def observe(self, raw: str):
        return observe_from_parse(self.stack_id, raw, detail="stub: parse-path only")
