from sipdrift import __version__
from sipdrift.parse import split_start_line


def test_version_pinned():
    assert __version__ == "0.0.1"


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
