"""Tests for stack drivers."""

from sipdrift.drivers.builtin import BuiltinDriver
from sipdrift.drivers.pjsip_stub import PjsipStubDriver
from sipdrift.fixtures import load_fixture


def test_builtin_driver_f200():
    raw = load_fixture("F-200-MIN")
    obs = BuiltinDriver().observe(raw)
    assert obs.ok is True
    assert obs.start_line == "SIP/2.0 200 OK"


def test_pjsip_stub_driver_f200():
    raw = load_fixture("F-200-MIN")
    obs = PjsipStubDriver().observe(raw)
    assert obs.ok is True
    assert obs.start_line == "SIP/2.0 200 OK"


def test_builtin_driver_malformed():
    raw = load_fixture("F-MALFORMED-START")
    obs = BuiltinDriver().observe(raw)
    assert obs.ok is False
    assert obs.start_line is None


def test_pjsip_stub_driver_malformed():
    raw = load_fixture("F-MALFORMED-START")
    obs = PjsipStubDriver().observe(raw)
    assert obs.ok is False
    assert obs.start_line is None


def test_fixture_start_lines():
    cases = {
        "F-486-MIN": "SIP/2.0 486 Busy Here",
        "F-503-MIN": "SIP/2.0 503 Service Unavailable",
        "F-OPTIONS-MIN": "OPTIONS sip:bob@example.com SIP/2.0",
        "F-REGISTER-MIN": "REGISTER sip:example.com SIP/2.0",
    }
    driver = BuiltinDriver()
    for fixture_id, expected in cases.items():
        raw = load_fixture(fixture_id)
        obs = driver.observe(raw)
        assert obs.ok is True
        assert obs.start_line == expected
