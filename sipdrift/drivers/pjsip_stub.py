"""PJSIP-target stack driver stub.

PJSIP (https://www.pjsip.org/) is GPL-2.0. Phase 1 uses the same parse path
as the builtin reference; a future lab driver will invoke pjsua/subprocess on
the Lab Test Server and replace this stub's observe() body.
"""

from __future__ import annotations

from sipdrift.harness import StackObservation
from sipdrift.parse import split_start_line


class PjsipStubDriver:
    """OSS-target stub for PJSIP — parse-path only until lab subprocess lands."""

    @property
    def stack_id(self) -> str:
        return "pjsip-stub"

    def observe(self, raw: str) -> StackObservation:
        # Hook point: subprocess to pjsua / pjproject test harness (Phase 2).
        try:
            start = split_start_line(raw)
        except ValueError as exc:
            return StackObservation(
                stack_id=self.stack_id,
                start_line=None,
                ok=False,
                detail=str(exc),
            )
        return StackObservation(
            stack_id=self.stack_id,
            start_line=start.raw,
            ok=True,
            detail="stub: parse-path only",
        )
