"""Sofia-SIP lab driver — subprocess to tools/sofia_observe."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from sipdrift.harness import StackObservation

_DEFAULT_BIN = Path(__file__).resolve().parents[2] / "tools" / "sofia_observe"


class SofiaLabDriver:
    """Real Sofia-SIP parse path via C helper on Lab hosts."""

    def __init__(self, binary: str | Path | None = None) -> None:
        env = os.environ.get("SIPDRIFT_SOFIA_OBSERVE", "").strip()
        self._bin = Path(env) if env else Path(binary) if binary else _DEFAULT_BIN

    @property
    def stack_id(self) -> str:
        return "sofia-lab"

    def observe(self, raw: str) -> StackObservation:
        if not self._bin.is_file():
            return StackObservation(
                stack_id=self.stack_id,
                start_line=None,
                ok=False,
                detail=f"sofia_observe missing: {self._bin}",
            )
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".sip",
            delete=False,
            newline="\n",
        ) as tmp:
            # Prefer CRLF for SIP wire; helper accepts either.
            tmp.write(raw.replace("\n", "\r\n") if "\r\n" not in raw else raw)
            path = tmp.name
        try:
            proc = subprocess.run(
                [str(self._bin), path],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return StackObservation(
                stack_id=self.stack_id,
                start_line=None,
                ok=False,
                detail=str(exc),
            )
        finally:
            try:
                Path(path).unlink(missing_ok=True)
            except OSError:
                pass

        line = (proc.stdout or "").strip().splitlines()
        json_line = ""
        for candidate in reversed(line):
            if candidate.startswith("{"):
                json_line = candidate
                break
        if not json_line:
            return StackObservation(
                stack_id=self.stack_id,
                start_line=None,
                ok=False,
                detail=f"no json line rc={proc.returncode} err={(proc.stderr or '')[:200]}",
            )
        try:
            data = json.loads(json_line)
        except json.JSONDecodeError as exc:
            return StackObservation(
                stack_id=self.stack_id,
                start_line=None,
                ok=False,
                detail=f"json parse: {exc}; raw={json_line[:200]}",
            )
        return StackObservation(
            stack_id=self.stack_id,
            start_line=data.get("start_line"),
            status_code=data.get("status_code"),
            via=data.get("via"),
            cseq=data.get("cseq"),
            ok=bool(data.get("ok")),
            detail=str(data.get("detail") or "sofia-lab"),
        )
