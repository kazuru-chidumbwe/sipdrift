"""Tests for compare run loop and CLI."""

import json

from sipdrift.cli import main
from sipdrift.drivers.builtin import BuiltinDriver
from sipdrift.drivers.pjsip_stub import PjsipStubDriver
from sipdrift.drivers.sofia_stub import SofiaStubDriver
from sipdrift.harness import CompareStatus
from sipdrift.run import case_to_dict, format_report, run_compare, run_suite


def test_run_compare_agree_f200():
    case = run_compare("F-200-MIN", BuiltinDriver(), PjsipStubDriver())
    assert case.status == CompareStatus.AGREE
    assert case.left.start_line == "SIP/2.0 200 OK"
    assert case.right.start_line == "SIP/2.0 200 OK"


def test_run_compare_error_malformed():
    case = run_compare("F-MALFORMED-START", BuiltinDriver(), PjsipStubDriver())
    assert case.status == CompareStatus.ERROR
    assert case.left.ok is False
    assert case.right.ok is False


def test_format_report_json():
    case = run_compare("F-200-MIN", BuiltinDriver(), PjsipStubDriver())
    text = format_report(case, fmt="json")
    data = json.loads(text)
    assert data["status"] == "agree"
    assert data["fixture_id"] == "F-200-MIN"
    assert data["left"]["stack_id"] == "builtin"
    assert data["right"]["stack_id"] == "pjsip-stub"


def test_case_to_dict_keys():
    case = run_compare("F-200-MIN", BuiltinDriver(), PjsipStubDriver())
    data = case_to_dict(case)
    assert set(data) == {"fixture_id", "status", "left", "right", "notes"}


def test_cli_compare_agree(capsys):
    code = main(["compare", "F-200-MIN"])
    assert code == 0
    out = capsys.readouterr().out
    assert "status:  agree" in out


def test_cli_compare_json(capsys):
    code = main(["compare", "F-200-MIN", "--format", "json"])
    assert code == 0
    data = json.loads(capsys.readouterr().out)
    assert data["status"] == "agree"


def test_cli_compare_malformed_error(capsys):
    code = main(["compare", "F-MALFORMED-START"])
    assert code == 1
    out = capsys.readouterr().out
    assert "status:  error" in out


def test_cli_unknown_driver():
    code = main(["compare", "F-200-MIN", "--left", "no-such-driver"])
    assert code == 2


def test_cli_unknown_fixture():
    code = main(["compare", "F-NOPE"])
    assert code == 2


def test_run_suite_default_pair():
    cases = run_suite(BuiltinDriver(), PjsipStubDriver())
    assert len(cases) >= 7
    agree = [c for c in cases if c.status == CompareStatus.AGREE]
    error = [c for c in cases if c.status == CompareStatus.ERROR]
    assert len(agree) >= 6
    assert any(c.fixture_id == "F-MALFORMED-START" for c in error)


def test_cli_suite(capsys):
    code = main(["suite", "--right", "sofia-stub"])
    assert code == 1  # malformed fixture errors
    out = capsys.readouterr().out
    assert "suite summary:" in out


def test_cross_oss_stubs_agree():
    case = run_compare("F-200-MIN", PjsipStubDriver(), SofiaStubDriver())
    assert case.status == CompareStatus.AGREE
