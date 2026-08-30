"""Internal reference driver — not an OSS SIP stack."""

from __future__ import annotations

from sipdrift.harness import StackObservation
from sipdrift.parse import split_start_line


class BuiltinDriver:
    """Parse fixture start-line as the reference observation."""

    @property
    def stack_id(self) -> str:
        return "builtin"

    def observe(self, raw: str) -> StackObservation:
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
        )
