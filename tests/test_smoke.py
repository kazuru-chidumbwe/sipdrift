from sipdrift import __version__
from sipdrift.fixtures import load_fixture
from sipdrift.harness import CompareStatus, StackObservation, classify_start_lines
from sipdrift.parse import split_start_line


def test_version_pinned():
    assert __version__ == "0.3.2"


def test_split_start_line_request():
    msg = "INVITE sip:bob@example.com SIP/2.0\r\nVia: SIP/2.0/UDP host\r\n\r\n"
    start = split_start_line(msg)
    assert start.raw.startswith("INVITE ")


def test_split_start_line_rejects_empty():
    try:
        split_start_line("\n\n")
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_load_invite_fixture():
    raw = load_fixture("F-INVITE-MIN")
    start = split_start_line(raw)
    assert start.raw.startswith("INVITE ")


def test_classify_agree_on_matching_start_lines():
    left = StackObservation(stack_id="A", start_line="SIP/2.0 200 OK", ok=True)
    right = StackObservation(stack_id="B", start_line="SIP/2.0 200 OK", ok=True)
    case = classify_start_lines("F-200-MIN", left, right)
    assert case.status == CompareStatus.AGREE


def test_classify_diverge_on_mismatch():
    left = StackObservation(stack_id="A", start_line="SIP/2.0 200 OK", ok=True)
    right = StackObservation(stack_id="B", start_line="SIP/2.0 486 Busy Here", ok=True)
    case = classify_start_lines("F-200-MIN", left, right)
    assert case.status == CompareStatus.DIVERGE
