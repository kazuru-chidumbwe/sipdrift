"""Driver registry — name to StackDriver instance."""

from __future__ import annotations

from sipdrift.drivers.builtin import BuiltinDriver
from sipdrift.drivers.pjsip_lab import PjsipLabDriver
from sipdrift.drivers.pjsip_stub import PjsipStubDriver
from sipdrift.drivers.protocol import StackDriver
from sipdrift.drivers.sofia_lab import SofiaLabDriver
from sipdrift.drivers.sofia_stub import SofiaStubDriver

_BUILTIN = BuiltinDriver()
_PJSIP_STUB = PjsipStubDriver()
_PJSIP_LAB = PjsipLabDriver()
_SOFIA_STUB = SofiaStubDriver()
_SOFIA_LAB = SofiaLabDriver()

DRIVERS: dict[str, StackDriver] = {
    _BUILTIN.stack_id: _BUILTIN,
    _PJSIP_STUB.stack_id: _PJSIP_STUB,
    _PJSIP_LAB.stack_id: _PJSIP_LAB,
    _SOFIA_STUB.stack_id: _SOFIA_STUB,
    _SOFIA_LAB.stack_id: _SOFIA_LAB,
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
