"""Kamailio-target stub driver (parse-path)."""

from __future__ import annotations

from sipdrift.drivers.common import observe_from_parse


class KamailioStubDriver:
    """OSS-target stub for Kamailio — parse-path until lab UDP observe is used."""

    @property
    def stack_id(self) -> str:
        return "kamailio-stub"

    def observe(self, raw: str):
        return observe_from_parse(self.stack_id, raw, detail="stub: parse-path only")
