"""Build StackObservation from lab JSON + optional wire body axes."""

from __future__ import annotations

from typing import Any

from sipdrift.harness import StackObservation
from sipdrift.parse import extract_body_axes


def observation_from_lab_json(
    stack_id: str,
    data: dict[str, Any],
    raw: str | None = None,
    default_detail: str = "",
) -> StackObservation:
    """Map lab helper JSON into StackObservation; fill body axes from wire if absent."""
    ctype = data.get("content_type")
    clen = data.get("content_length")
    body_hash = data.get("body_sha256")
    sdp_hash = data.get("sdp_sha256")
    if raw is not None and (
        body_hash is None or sdp_hash is None or ctype is None or clen is None
    ):
        w_ctype, w_clen, w_body, w_sdp = extract_body_axes(raw)
        if ctype is None:
            ctype = w_ctype
        if clen is None:
            clen = w_clen
        if body_hash is None:
            body_hash = w_body
        if sdp_hash is None:
            sdp_hash = w_sdp

    clen_int: int | None
    if clen is None or isinstance(clen, int):
        clen_int = clen
    else:
        try:
            clen_int = int(clen)
        except (TypeError, ValueError):
            clen_int = None

    return StackObservation(
        stack_id=stack_id,
        start_line=data.get("start_line"),
        status_code=data.get("status_code"),
        via=data.get("via"),
        cseq=data.get("cseq"),
        content_type=ctype,
        content_length=clen_int,
        body_sha256=body_hash,
        sdp_sha256=sdp_hash,
        ok=bool(data.get("ok")),
        detail=str(data.get("detail") or default_detail),
    )
