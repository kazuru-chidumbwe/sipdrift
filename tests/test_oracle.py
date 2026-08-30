"""Tests for multi-axis classification."""

from sipdrift.harness import CompareStatus, StackObservation, classify_observations


def test_classify_agree_all_axes():
    left = StackObservation(
        stack_id="A",
        start_line="SIP/2.0 200 OK",
        status_code=200,
        via="SIP/2.0/UDP host",
        cseq="1 INVITE",
        ok=True,
    )
    right = StackObservation(
        stack_id="B",
        start_line="SIP/2.0 200 OK",
        status_code=200,
        via="SIP/2.0/UDP host",
        cseq="1 INVITE",
        ok=True,
    )
    case = classify_observations("F-200-MIN", left, right)
    assert case.status == CompareStatus.AGREE


def test_classify_diverge_on_via():
    left = StackObservation(
        stack_id="A",
        start_line="SIP/2.0 200 OK",
        status_code=200,
        via="branch=a",
        cseq="1 INVITE",
        ok=True,
    )
    right = StackObservation(
        stack_id="B",
        start_line="SIP/2.0 200 OK",
        status_code=200,
        via="branch=b",
        cseq="1 INVITE",
        ok=True,
    )
    case = classify_observations("F-200-MIN", left, right)
    assert case.status == CompareStatus.DIVERGE
    assert any("via mismatch" in note for note in case.notes)
