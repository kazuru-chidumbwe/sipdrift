"""Kamailio lab driver — UDP fixture to local kamailio observe listener."""

from __future__ import annotations

import json
import os
import socket
import time
from pathlib import Path

from sipdrift.harness import StackObservation

_DEFAULT_OBS = Path("/tmp/sipdrift-kamailio-obs.json")
_DEFAULT_HOST = "127.0.0.1"
_DEFAULT_PORT = 5090


class KamailioLabDriver:
    """Proxy-tier lab driver: send fixture UDP → Kamailio Lua dumps JSON axes."""

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        obs_path: str | Path | None = None,
    ) -> None:
        self._host = host or os.environ.get("SIPDRIFT_KAMAILIO_HOST", _DEFAULT_HOST)
        env_port = os.environ.get("SIPDRIFT_KAMAILIO_PORT", "").strip()
        self._port = port if port is not None else int(env_port or _DEFAULT_PORT)
        env_obs = os.environ.get("SIPDRIFT_KAMAILIO_OBS", "").strip()
        self._obs = Path(obs_path) if obs_path else Path(env_obs) if env_obs else _DEFAULT_OBS

    @property
    def stack_id(self) -> str:
        return "kamailio-lab"

    def observe(self, raw: str) -> StackObservation:
        wire = raw.replace("\n", "\r\n") if "\r\n" not in raw else raw
        payload = wire.encode("utf-8", errors="replace")
        try:
            if self._obs.exists():
                self._obs.unlink()
        except OSError:
            pass

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2.0)
            sock.sendto(payload, (self._host, self._port))
            sock.close()
        except OSError as exc:
            return StackObservation(
                stack_id=self.stack_id,
                start_line=None,
                ok=False,
                detail=f"udp send failed: {exc}",
            )

        deadline = time.time() + 2.5
        data = None
        while time.time() < deadline:
            if self._obs.is_file() and self._obs.stat().st_size > 0:
                try:
                    text = self._obs.read_text(encoding="utf-8", errors="replace").strip()
                    if text:
                        data = json.loads(text.splitlines()[-1])
                        break
                except (OSError, json.JSONDecodeError):
                    pass
            time.sleep(0.05)

        if not data:
            return StackObservation(
                stack_id=self.stack_id,
                start_line=None,
                ok=False,
                detail=f"no observation file from kamailio at {self._obs}",
            )

        return StackObservation(
            stack_id=self.stack_id,
            start_line=data.get("start_line"),
            status_code=data.get("status_code"),
            via=data.get("via"),
            cseq=data.get("cseq"),
            ok=bool(data.get("ok")),
            detail=str(data.get("detail") or "kamailio-lab"),
        )
