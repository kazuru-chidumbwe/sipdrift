"""Internal reference driver — not an OSS SIP stack."""

from __future__ import annotations

from sipdrift.drivers.common import observe_from_parse


class BuiltinDriver:
    """Parse fixture axes as the reference observation."""

    @property
    def stack_id(self) -> str:
        return "builtin"

    def observe(self, raw: str):
        return observe_from_parse(self.stack_id, raw)
