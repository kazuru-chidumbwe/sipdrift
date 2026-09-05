#!/usr/bin/env python3
"""Host B experiment matrix for sipdrift — run many compare/suite packs."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sipdrift.drivers.registry import get_driver, list_driver_names  # noqa: E402
from sipdrift.fixtures import FIXTURE_INDEX  # noqa: E402
from sipdrift.run import run_compare, run_suite, suite_to_dict  # noqa: E402


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_cmd(cmd: list[str], timeout: int = 30) -> dict:
    started = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        return {
            "cmd": cmd,
            "rc": proc.returncode,
            "stdout": (proc.stdout or "")[:4000],
            "stderr": (proc.stderr or "")[:2000],
            "elapsed_s": round(time.time() - started, 3),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "cmd": cmd,
            "rc": -1,
            "stdout": (exc.stdout or "")[:2000] if isinstance(exc.stdout, str) else "",
            "stderr": f"timeout after {timeout}s",
            "elapsed_s": round(time.time() - started, 3),
        }


def main() -> int:
    pack_id = f"sipdrift-hostb-{utc_stamp()}"
    out = Path(os.environ.get("SIPDRIFT_PACK_DIR", f"/opt/atlas/sipdrift-packs/{pack_id}"))
    out.mkdir(parents=True, exist_ok=True)

    experiments: list[dict] = []
    drivers = list_driver_names()
    fixtures = list(FIXTURE_INDEX)

    meta = {
        "pack_id": pack_id,
        "host": socket.gethostname(),
        "host_ip_hint": "10.4.0.32",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "drivers": drivers,
        "fixture_count": len(fixtures),
        "fixtures": fixtures,
    }
    write_json(out / "meta.json", meta)

    # E1: every driver pair suite
    pairs = []
    for left in drivers:
        for right in drivers:
            if left == right:
                continue
            pairs.append((left, right))

    for i, (left, right) in enumerate(pairs, 1):
        name = f"E-suite-{left}-vs-{right}"
        cases = run_suite(get_driver(left), get_driver(right))
        payload = suite_to_dict(cases)
        payload["experiment"] = name
        payload["left"] = left
        payload["right"] = right
        write_json(out / f"{name}.json", payload)
        experiments.append(
            {
                "id": name,
                "kind": "suite",
                "left": left,
                "right": right,
                "summary": payload["summary"],
                "n_cases": len(cases),
            }
        )
        print(f"[{i}/{len(pairs)}] {name} -> {payload['summary']}", flush=True)

    # E2: per-fixture spotlight on builtin vs sofia-lab (if present)
    spotlight_right = "sofia-lab" if "sofia-lab" in drivers else "sofia-stub"
    for fid in fixtures:
        name = f"E-compare-builtin-vs-{spotlight_right}-{fid}"
        case = run_compare(fid, get_driver("builtin"), get_driver(spotlight_right))
        payload = {
            "experiment": name,
            "fixture_id": fid,
            "status": case.status.value,
            "notes": case.notes,
            "left": {
                "stack_id": case.left.stack_id,
                "ok": case.left.ok,
                "start_line": case.left.start_line,
                "status_code": case.left.status_code,
                "via": case.left.via,
                "cseq": case.left.cseq,
                "detail": case.left.detail,
            },
            "right": {
                "stack_id": case.right.stack_id,
                "ok": case.right.ok,
                "start_line": case.right.start_line,
                "status_code": case.right.status_code,
                "via": case.right.via,
                "cseq": case.right.cseq,
                "detail": case.right.detail,
            },
        }
        write_json(out / f"{name}.json", payload)
        experiments.append(
            {
                "id": name,
                "kind": "compare",
                "fixture": fid,
                "status": case.status.value,
            }
        )

    # E3: Sofia CLI tool smokes
    tool_cmds = [
        ["sip-date"],
        ["localinfo"],
        ["addrinfo", "example.com"],
        ["sip-dig", "sip:example.com"],
        ["sip-options", "--help"],
        ["stunc", "--help"],
    ]
    for cmd in tool_cmds:
        name = f"E-tool-{cmd[0]}"
        result = run_cmd(cmd, timeout=15)
        write_json(out / f"{name}.json", {"experiment": name, **result})
        experiments.append({"id": name, "kind": "tool", "rc": result["rc"], "cmd": cmd})
        print(f"[tool] {name} rc={result['rc']}", flush=True)

    # E4: live OPTIONS against local UDP responder (spawned briefly)
    responder = ROOT / "tools" / "sip_udp_responder.py"
    if responder.is_file():
        port = 15060
        proc = subprocess.Popen(
            [sys.executable, str(responder), "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        time.sleep(0.5)
        try:
            for label, extra in [
                ("options-default", []),
                ("options-all", ["--all"]),
                ("options-method-info", ["--method=INFO"]),
            ]:
                name = f"E-live-{label}"
                cmd = ["sip-options", "-m", f"sip:*:{port}", f"sip:127.0.0.1:{port}", *extra]
                result = run_cmd(cmd, timeout=10)
                write_json(out / f"{name}.json", {"experiment": name, **result})
                experiments.append({"id": name, "kind": "live", "rc": result["rc"], "cmd": cmd})
                print(f"[live] {name} rc={result['rc']}", flush=True)
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()

    # E5: pytest regression on host
    name = "E-pytest"
    result = run_cmd([sys.executable, "-m", "pytest", "-q"], timeout=120)
    # run from ROOT
    result = run_cmd([sys.executable, "-m", "pytest", "-q"], timeout=120)
    # fix cwd
    started = time.time()
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    result = {
        "cmd": ["pytest", "-q"],
        "rc": proc.returncode,
        "stdout": (proc.stdout or "")[:4000],
        "stderr": (proc.stderr or "")[:2000],
        "elapsed_s": round(time.time() - started, 3),
    }
    write_json(out / f"{name}.json", {"experiment": name, **result})
    experiments.append({"id": name, "kind": "pytest", "rc": result["rc"]})
    print(f"[pytest] rc={result['rc']}", flush=True)

    summary = {
        "pack_id": pack_id,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "n_experiments": len(experiments),
        "experiments": experiments,
        "out_dir": str(out),
    }
    write_json(out / "EXPERIMENT-INDEX.json", summary)
    print(json.dumps({"pack_id": pack_id, "n": len(experiments), "out": str(out)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
