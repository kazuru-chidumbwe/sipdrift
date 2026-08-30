"""Stack driver protocol for SIP differential testing."""

from __future__ import annotations

from typing import Protocol

from sipdrift.harness import StackObservation


class StackDriver(Protocol):
    """Observe a SIP message fixture and return a normalized stack record."""

    @property
    def stack_id(self) -> str:
        """Stable identifier for reports and manifests."""
        ...

    def observe(self, raw: str) -> StackObservation:
        """Process fixture bytes and return a normalized observation."""
        ...
