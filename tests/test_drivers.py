"""Tests for stack drivers."""

from sipdrift.drivers.builtin import BuiltinDriver
from sipdrift.drivers.pjsip_stub import PjsipStubDriver
from sipdrift.drivers.sofia_stub import SofiaStubDriver
from sipdrift.fixtures import load_fixture


def test_builtin_driver_f200():
    raw = load_fixture("F-200-MIN")
    obs = BuiltinDriver().observe(raw)
    assert obs.ok is True
    assert obs.start_line == "SIP/2.0 200 OK"
    assert obs.status_code == 200
    assert obs.via is not None
    assert obs.cseq is not None


def test_pjsip_stub_driver_f200():
    raw = load_fixture("F-200-MIN")
    obs = PjsipStubDriver().observe(raw)
    assert obs.ok is True
    assert obs.start_line == "SIP/2.0 200 OK"
    assert obs.status_code == 200


def test_sofia_stub_driver_f200():
    raw = load_fixture("F-200-MIN")
    obs = SofiaStubDriver().observe(raw)
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
        "F-486-MIN": ("SIP/2.0 486 Busy Here", 486),
        "F-503-MIN": ("SIP/2.0 503 Service Unavailable", 503),
        "F-OPTIONS-MIN": ("OPTIONS sip:bob@example.com SIP/2.0", None),
        "F-REGISTER-MIN": ("REGISTER sip:example.com SIP/2.0", None),
    }
    driver = BuiltinDriver()
    for fixture_id, (expected_line, expected_status) in cases.items():
        raw = load_fixture(fixture_id)
        obs = driver.observe(raw)
        assert obs.ok is True
        assert obs.start_line == expected_line
        assert obs.status_code == expected_status


def test_oss_stubs_agree_on_axes():
    raw = load_fixture("F-200-MIN")
    left = PjsipStubDriver().observe(raw)
    right = SofiaStubDriver().observe(raw)
    assert left.start_line == right.start_line
    assert left.status_code == right.status_code
    assert left.via == right.via
    assert left.cseq == right.cseq
