"""Driver registry — name to StackDriver instance."""

from __future__ import annotations

from sipdrift.drivers.builtin import BuiltinDriver
from sipdrift.drivers.pjsip_stub import PjsipStubDriver
from sipdrift.drivers.protocol import StackDriver

_BUILTIN = BuiltinDriver()
_PJSIP_STUB = PjsipStubDriver()

DRIVERS: dict[str, StackDriver] = {
    _BUILTIN.stack_id: _BUILTIN,
    _PJSIP_STUB.stack_id: _PJSIP_STUB,
}


def get_driver(name: str) -> StackDriver:
    """Return a registered driver by name.

    Raises:
        KeyError: unknown driver name.
    """
    try:
        return DRIVERS[name]
    except KeyError as exc:
        known = ", ".join(sorted(DRIVERS))
        raise KeyError(f"unknown driver {name!r}; known: {known}") from exc


def list_driver_names() -> list[str]:
    """Return registered driver names in stable order."""
    return sorted(DRIVERS)
